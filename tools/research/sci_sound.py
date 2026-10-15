#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""SCI1 early sound directory/event reference exporter (no synthesizer).

Format/algorithm references: ScummVM, GPL-3.0-or-later, commit
2b5f9b5d95f267c87889746906148db6088130f8:
 engines/sci/resource/resource_audio.cpp (SoundResource constructor)
 engines/sci/sound/midiparser_sci.cpp (midiMixChannels, processEvent).
This narrow Python adaptation emits inspectable events and approximate Standard
MIDI Files, not original-hardware recordings or a complete SCI sound runtime.
"""
import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

REVISION = '2b5f9b5d95f267c87889746906148db6088130f8'
SOURCES = [f'https://github.com/scummvm/scummvm/blob/{REVISION}/{p}' for p in (
    'engines/sci/resource/resource_audio.cpp', 'engines/sci/sound/midiparser_sci.cpp')]
SOURCE_HASHES = {
    'engines/sci/resource/resource_audio.cpp': '0481aca313cf2373348952a1e47a501d90d1bea0adbb2b6d29ce15bf6dc72d3f',
    'engines/sci/sound/midiparser_sci.cpp': '0837730e78ab5fdb8dbd3cd419f26163a53f9dbd7913853945b5b63d9560785f'
}
LIMITATIONS = [
    'MIDI exports preserve one finite event pass; SCI loops, holds, cues and device voice mapping are not executed.',
    'Program numbers are original device-specific values, not General MIDI remappings; ordinary MIDI playback can sound different.',
    'SCI-specific commands are preserved in event JSON and represented as MIDI text markers, not sent as instrument controls.',
    'Timing uses the SCI nominal 60 ticks/second; no original-hardware audio synthesis or listening verification is performed.',
    'Digital channels and device type 0xF0 are catalogued but not exported as playable audio.'
]


def u16(data, offset):
    return struct.unpack_from('<H', data, offset)[0]


def parse_events(data):
    """Each SCI delta is one byte; F8 adds 240 ticks without an event."""
    pos, tick, running = 0, 0, None
    events = []
    while pos < len(data):
        delta = data[pos]
        pos += 1
        tick += 240 if delta == 0xF8 else delta
        if delta == 0xF8:
            continue
        if pos >= len(data):
            raise ValueError('missing event after delta')
        start = pos
        command = data[pos]
        pos += 1
        if command == 0xFC:
            events.append({'tick': tick, 'type': 'end', 'stream_offset': start})
            return events, pos
        if command == 0xF0:
            end = data.find(b'\xf7', pos)
            if end < 0:
                raise ValueError('unterminated sysex')
            events.append({'tick': tick, 'type': 'sysex', 'data_hex': data[pos:end + 1].hex(), 'stream_offset': start})
            pos = end + 1
            continue
        if command < 0x80:
            if running is None:
                raise ValueError('running status without prior channel command')
            pos -= 1
            command = running
        if not 0x80 <= command <= 0xEF:
            raise ValueError(f'unsupported system command {command:#x}')
        count = 1 if command >> 4 in (0xC, 0xD) else 2
        params = list(data[pos:pos + count])
        if len(params) != count or any(x > 127 for x in params):
            raise ValueError('truncated or invalid MIDI parameters')
        pos += count
        running = command
        kind = 'midi'
        if (command & 15) == 15 and (command >> 4) in (0xB, 0xC):
            kind = 'sci_control'
        elif command >> 4 == 0xB and params[0] in (0x4B, 0x4C, 0x4E, 0x50, 0x52, 0x60):
            kind = 'sci_control'
        events.append({'tick': tick, 'type': kind, 'status': command, 'channel': command & 15,
                       'parameters': params, 'stream_offset': start})
    raise ValueError('channel ended without SCI end marker')


def directory(data):
    pos, tracks = 0, []
    while pos < len(data):
        device = data[pos]
        pos += 1
        if device == 255:
            return tracks, pos
        channels = []
        while pos < len(data) and data[pos] != 255:
            if pos + 6 > len(data):
                raise ValueError('truncated device/channel directory')
            unknown, offset, size = struct.unpack_from('<HHH', data, pos)
            channels.append({'directory_word': unknown, 'offset': offset, 'size': size})
            pos += 6
        if pos >= len(data):
            raise ValueError('missing device terminator')
        pos += 1
        tracks.append({'device_type': device, 'device_type_hex': f'0x{device:02x}', 'channels': channels})
    raise ValueError('missing directory terminator')


def vlq(number):
    if number < 0:
        raise ValueError('negative MIDI delta')
    out = [number & 127]
    while number >> 7:
        number >>= 7
        out.insert(0, 128 | (number & 127))
    return bytes(out)


def midi_track(events, name):
    title = name.encode('ascii')
    out = bytearray(b'\x00\xff\x03' + vlq(len(title)) + title)
    previous = 0
    for event in events:
        tick = event['tick']
        if event['type'] == 'end':
            continue
        if event['type'] == 'midi':
            payload = bytes([event['status']] + event['parameters'])
        elif event['type'] == 'sysex':
            raw = bytes.fromhex(event['data_hex'])
            payload = b'\xf0' + vlq(len(raw)) + raw
        else:
            text = ('SCI ' + json.dumps(event, separators=(',', ':'))).encode('ascii')
            payload = b'\xff\x06' + vlq(len(text)) + text
        out += vlq(tick - previous) + payload
        previous = tick
    end = max([e['tick'] for e in events] + [previous])
    out += vlq(end - previous) + b'\xff\x2f\x00'
    return b'MTrk' + struct.pack('>I', len(out)) + out


def midi_file(channels):
    # PPQN 60, tempo 1,000,000 microseconds/quarter -> 60 SCI ticks/sec.
    conductor = b'\x00\xff\x51\x03\x0f\x42\x40\x00\xff\x2f\x00'
    tracks = [b'MTrk' + struct.pack('>I', len(conductor)) + conductor]
    tracks.extend(midi_track(c['events'], f"SCI channel {c['channel_number']}") for c in channels)
    return b'MThd' + struct.pack('>IHHH', 6, 1, len(tracks), 60) + b''.join(tracks)


def export_sounds(rawdir, outdir):
    rawdir, outdir = Path(rawdir), Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted(rawdir.glob('sound.*.bin')):
        data = path.read_bytes()
        record = {'resource_id': int(path.stem.split('.')[1]), 'input_file': path.name,
                  'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        try:
            tracks, header_size = directory(data)
            record.update({'status': 'directory_and_events_decoded', 'directory_bytes': header_size, 'tracks': tracks})
            for ti, track in enumerate(tracks):
                decoded = []
                for channel in track['channels']:
                    offset, size = channel['offset'], channel['size']
                    try:
                        if offset < header_size or size < 2 or offset + size > len(data):
                            raise ValueError('channel offset/size outside payload or overlaps directory')
                        blob = data[offset:offset + size]
                        number, poly = blob[:2]
                        if track['device_type'] == 0xF0:
                            channel['status'] = 'unsupported_digital_track_directory'
                            continue
                        channel.update({'channel_number': number & 15, 'flags': number >> 4,
                                        'polyphony': poly & 15, 'priority': poly >> 4})
                        if number == 0xFE:
                            channel['status'] = 'digital_channel_metadata_only'
                            if len(blob) >= 10:
                                channel['digital'] = dict(zip(['rate_hz','sample_size','sample_start','sample_end'], struct.unpack_from('<HHHH', blob, 2)))
                            continue
                        events, consumed = parse_events(blob[2:])
                        channel.update({'status': 'events_decoded', 'event_count': len(events),
                                        'event_types': dict(Counter(e['type'] for e in events)),
                                        'duration_ticks': events[-1]['tick'], 'duration_seconds_nominal': events[-1]['tick'] / 60,
                                        'bytes_consumed': consumed + 2, 'trailing_bytes': size - consumed - 2,
                                        'events': events})
                        decoded.append(channel)
                    except (ValueError, IndexError, struct.error) as exc:
                        channel.update({'status': 'unsupported_or_invalid', 'error': str(exc)})
                playable = [c for c in track['channels'] if c.get('status') == 'events_decoded']
                if playable:
                    name = f"sound.{record['resource_id']:03d}.device-{track['device_type']:02x}.track-{ti}.mid"
                    (outdir / name).write_bytes(midi_file(playable))
                    track['midi_file'] = name
                    track['midi_status'] = 'finite_event_reference_not_hardware_audio'
                track['status'] = 'events_decoded' if len(decoded) == len(track['channels']) else 'partial_or_metadata_only'
            if any(t['status'] != 'events_decoded' for t in tracks):
                record['status'] = 'partial_or_metadata_only'
            event_name = f"sound.{record['resource_id']:03d}.events.json"
            (outdir / event_name).write_text(json.dumps(record, indent=2) + '\n')
            record['events_file'] = event_name
            # Keep the aggregate compact. Full event data stays in the per-resource JSON.
            for track in tracks:
                for channel in track['channels']:
                    channel.pop('events', None)
        except (ValueError, IndexError, struct.error) as exc:
            record.update({'status': 'unsupported_or_invalid', 'error': str(exc)})
        records.append(record)
    manifest = {'format': 'SCI1early', 'reference_revision': REVISION, 'source_urls': SOURCES,
                'reference_source_sha256': SOURCE_HASHES,
                'exporter_license': 'GPL-3.0-or-later', 'limitations': LIMITATIONS, 'sounds': records}
    (outdir / 'sound-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw_dir', type=Path)
    parser.add_argument('output_dir', type=Path)
    args = parser.parse_args()
    records = export_sounds(args.raw_dir, args.output_dir)
    print(json.dumps({'sounds': len(records), 'statuses': dict(Counter(r['status'] for r in records)),
                      'midi_exports': sum('midi_file' in t for r in records for t in r.get('tracks', []))}))
