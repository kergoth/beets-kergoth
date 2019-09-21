Verify that beets works

Set up initial beets configuration

  $ export BEETSDIR="$PWD"
  $ beet version >/dev/null

  $ cat >"$PWD/config.yaml" <<END
  > directory: .
  > plugins: savedqueries
  > album_queries:
  >   is_blank: "album:'Blank Audio'"
  >   no_total: "albumtotal::^0$"
  >   foo: "albumartist:foo"
  > item_queries:
  >   '250': "title:250"
  > END

Set up library

  $ beet import -qCWA "$TESTDIR/data/250-milliseconds-of-silence.mp3" >/dev/null 2>&1
  $ beet ls
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Album queries

  $ beet ls -a album_query:foo
  $ beet ls -a album_query:is_blank
  Anar Software LLC - Blank Audio
  $ beet ls -a -f '$albumtotal'
  0
  $ beet ls -a album_query:no_total
  Anar Software LLC - Blank Audio

Album query fields

  $ beet ls -a -f '$is_blank $no_total $foo'
  True True False

Querying the saved query fields is slow, but possible

  $ beet ls -a is_blank:1
  Anar Software LLC - Blank Audio
  $ beet ls -a foo:1

Item queries

  $ beet ls query:250
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence

Item query fields

  $ beet ls -f '$250'
  True

Querying the saved query fields is slow, but possible

  $ beet ls 250:1
  Anar Software LLC - Blank Audio - 250 Milliseconds of Silence
