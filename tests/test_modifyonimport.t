# Verify that beets works

# Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

# Test config error handling

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: modifyonimport
  > modifyonimport:
  >   modify_album:
  >     '': 'wrong_query:foo'
  > END
  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  error: modifyonimport.modify_album[""]: unexpected query `wrong_query:foo` in value
  [1]
  $ rm -f library.db

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: modifyonimport
  > modifyonimport:
  >   modify_album:
  >     foo: ''
  > END
  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3"
  error: modifyonimport.modify_album["foo"]: no modifications found
  [1]
  $ rm -f library.db

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > ui:
  >   color: no
  > plugins: modifyonimport
  > modifyonimport:
  >   modify_album:
  >     '': flexfield=1
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
  .*/data/250-milliseconds-of-silence.mp3 (re)
  Anar Software LLC - Blank Audio
    albumartist: Anar Software LLC -> Foo
    flexfield: 1
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
    artist: Anar Software LLC -> Modified
  $ beet ls -a -f '$albumartist - $album - $flexfield'
  Foo - Blank Audio - 1
  $ beet ls
  Modified - Blank Audio - 250 Milliseconds of Silence

Reset library

  $ rm library.db

Test singleton

  $ beet import -qsCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" | grep '\->' | sort
  .*/data/250-milliseconds-of-silence.mp3 (re)
    artist_credit:  -> Bar
    artist_sort:  -> Bar
  $ beet ls -f '$artist $artist_sort $artist_credit'
  Anar Software LLC Bar Bar

Test file move based on modified metadata

  $ rm -f library.db; cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: modifyonimport
  > modifyonimport:
  >   modify_singleton:
  >     silence: title=Blah
  > END
  $ beet import -qscwA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null
  .*/data/250-milliseconds-of-silence.mp3 (re)
  $ beet ls -p
  .*/Blah.mp3 (re)
