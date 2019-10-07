Verify that beets works

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > pluginpath:
  >   - $TESTDIR/beetsplug
  > plugins: mockedcandidate importinspect
  > END

Test initial import confirmation on apply

  $ (echo a; echo y;) |  beet import -CWa -S mocked "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  
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
    album: Blank Audio -> An Album
    albumartist: Anar Software LLC -> An Artist
    country:  -> XW
    day: 00 -> 01
    disctotal: 00 -> 01
    mb_albumartistid:  -> http://foo
    mb_albumid:  -> mocked
    month: 00 -> 01
    year: 0000 -> 2019
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist: Anar Software LLC -> An Artist
    disc: 00 -> 01
    mb_artistid:  -> 1
    mb_trackid:  -> http://foo
    media:  -> Digital Media
    title: 250 Milliseconds of Silence -> A Track
    tracktotal: 00 -> 01




Set up library again to test re-import

  $ rm library.db
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
    album: Blank Audio -> An Album
    albumartist: Anar Software LLC -> An Artist
    country:  -> XW
    day: 00 -> 01
    disctotal: 00 -> 01
    mb_albumartistid:  -> http://foo
    mb_albumid:  -> mocked
    month: 00 -> 01
    year: 0000 -> 2019
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist: Anar Software LLC -> An Artist
    disc: 00 -> 01
    mb_artistid:  -> 1
    mb_trackid:  -> http://foo
    media:  -> Digital Media
    title: 250 Milliseconds of Silence -> A Track
    tracktotal: 00 -> 01
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
    album: Blank Audio -> An Album
    albumartist: Anar Software LLC -> An Artist
    country:  -> XW
    day: 00 -> 01
    disctotal: 00 -> 01
    mb_albumartistid:  -> http://foo
    mb_albumid:  -> mocked
    month: 00 -> 01
    year: 0000 -> 2019
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist: Anar Software LLC -> An Artist
    disc: 00 -> 01
    mb_artistid:  -> 1
    mb_trackid:  -> http://foo
    media:  -> Digital Media
    title: 250 Milliseconds of Silence -> A Track
    tracktotal: 00 -> 01


