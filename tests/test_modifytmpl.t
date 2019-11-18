Verify that beets works

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: modifytmpl the
  > END

Test with album

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Test referencing other fields

  $ beet modifytmpl -yW id:1 artist_credit::'^$' artist_credit='$artist'
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist_credit:  -> Anar Software LLC

Test use of a format function

  $ beet modify -yaW id:1 albumartist='The Test'
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    albumartist: Anar Software LLC -> The Test

  $ beet modifytmpl -yaW id:1 albumartist_sort='%the{$albumartist}'
  Modifying 1 albums.
  The Test - Blank Audio
    albumartist_sort:  -> Test, The

Test with prompt

  $ echo y | beet modifytmpl -W id:1 testfield='$album'
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    testfield: Blank Audio
  Really modify and move? (Yes/no/select) 

Test warning when modifying album fields on an item

  $ echo n | beet modifytmpl -yW id:1 albumartist=Foo
  modifytmpl: modification of album field `albumartist` should be done on the album, not the item
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    albumartist: The Test -> Foo
  Really modify and move? (Yes/no/select) 

Test warning when modifying item fields on an album

  $ echo n | beet modifytmpl -yaW id:1 tracktotal=1
  modifytmpl: modification of non-album field `tracktotal` should be done on the item, not the album
  Modifying 1 albums.
  The Test - Blank Audio
    tracktotal: 1
  Really modify and move? (Yes/no/select) 

Test error when modifying computed fields

  $ beet modifytmpl -yW id:1 samplerate=100
  error: modification or deletion of computed field `samplerate` is not supported
  [1]
