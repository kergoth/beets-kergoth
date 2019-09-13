# Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: alias mockedcandidate picard
  > alias:
  >   aliases:
  >     picard: '!echo picard me'
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1

Picard me

  $ beet picard
  picard me
  $ (echo p; echo b;) | beet import -L -S mocked id:1
  
  /.* \(1 items\) (re)
  Correcting tags from:
      Anar Software LLC - Blank Audio
  To:
      An Artist - An Album
  URL:
      http://invalid
  (Similarity: 37.5%) (album, artist, tracks, source) (mocked_candidate, Digital Media, 2019, XW)
   * 250 Milliseconds of Silence (#0) -> A Track (#None) (title)
  Apply, More candidates, Skip, Use as-is, as Tracks, Group albums,
  Enter search, enter Id, aBort, Picard\? picard me /.*/data/250-milliseconds-of-silence.mp3 (re)
  Correcting tags from:
      Anar Software LLC - Blank Audio
  To:
      An Artist - An Album
  URL:
      http://invalid
  (Similarity: 37.5%) (album, artist, tracks, source) (mocked_candidate, Digital Media, 2019, XW)
   * 250 Milliseconds of Silence (#0) -> A Track (#None) (title)
  Apply, More candidates, Skip, Use as-is, as Tracks, Group albums,
  Enter search, enter Id, aBort, Picard?  (no-eol)


