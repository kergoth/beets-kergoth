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
  > plugins: modifyonimport
  > import:
  >   quiet_fallback: skip
  > modifyonimport:
  >   modify_album:
  >     blank: 'albumartist=Foo'
  >   modify_album_items:
  >     blank:
  >       '250': artist=Modified
  >       'invalid': artist=ModifiedMore
  >     nothing:
  >       '250': artist=ModifiedNothing
  >   modify_singleton:
  >     '250': artist_sort=Bar artist_credit=Bar
  > END

Test album and album_items

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  /Users/kergoth/Repos/github.com/kergoth/beets-kergoth/tests/data/250-milliseconds-of-silence.mp3
  Modifying 1 albums.
  Anar Software LLC - Blank Audio
    albumartist: Anar Software LLC -> Foo
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist: Anar Software LLC -> Modified
  $ beet ls -a
  Foo - Blank Audio
  $ beet ls
  Modified - Blank Audio - 250 Milliseconds of Silence

Reset library

  $ beet rm -fa id:1

Test singleton

  $ beet import -qsCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  /Users/kergoth/Repos/github.com/kergoth/beets-kergoth/tests/data/250-milliseconds-of-silence.mp3
  Modifying 1 items.
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist_sort:  -> Bar
    artist_credit:  -> Bar
  $ beet ls -f '$artist $artist_sort $artist_credit'
  Anar Software LLC Bar Bar
