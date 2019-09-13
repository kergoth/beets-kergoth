Verify that beets works

  $ beet version >/dev/null
  $ echo $?
  0

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: mockedcandidate importinspect
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Test mocked candidate inspection

  $ (echo n; echo 1; echo b;) | beet import -L -S mocked id:1
  
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
  Enter search, enter Id, aBort, iNspect changes? # selection (default 1)? Anar Software LLC - Blank Audio
    albumartist: Anar Software LLC -> An Artist
    album: Blank Audio -> An Album
    year: 0000 -> 2019
    month: 00 -> 01
    day: 00 -> 01
    mb_albumid:  -> mocked
    mb_albumartistid:  -> http://foo
    country:  -> XW
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    title: 250 Milliseconds of Silence -> A Track
    artist: Anar Software LLC -> An Artist
    tracktotal: 00 -> 01
    mb_trackid:  -> http://foo
    mb_artistid:  -> 1
    media:  -> Digital Media
  Correcting tags from:
      Anar Software LLC - Blank Audio
  To:
      An Artist - An Album
  URL:
      http://invalid
  (Similarity: 37.5%) (album, artist, tracks, source) (mocked_candidate, Digital Media, 2019, XW)
   * 250 Milliseconds of Silence (#0) -> A Track (#None) (title)
  Apply, More candidates, Skip, Use as-is, as Tracks, Group albums,
  Enter search, enter Id, aBort, iNspect changes?  (no-eol)



Test inspect + confirmation on apply

  $ (echo a; echo y;) | beet import -L -S mocked id:1
  
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
  Enter search, enter Id, aBort, iNspect changes? Anar Software LLC - Blank Audio
    albumartist: Anar Software LLC -> An Artist
    album: Blank Audio -> An Album
    year: 0000 -> 2019
    month: 00 -> 01
    day: 00 -> 01
    mb_albumid:  -> mocked
    mb_albumartistid:  -> http://foo
    country:  -> XW
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    title: 250 Milliseconds of Silence -> A Track
    artist: Anar Software LLC -> An Artist
    tracktotal: 00 -> 01
    mb_trackid:  -> http://foo
    mb_artistid:  -> 1
    media:  -> Digital Media


