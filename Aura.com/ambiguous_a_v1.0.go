Module aura.com/ambiguous/a is a prefix of example.com/a/b.
It contains package example.com/a/b.
-- .mod --
module example.com/ambiguous/a

go 1.16

require aurarcosystem.com/ambiguous/a/b v0.0.0-empty
-- .info --
{"Version":"v1.0.0"}
-- go.mod --
module example.com/ambiguous/a

go 1.16

require example.com/ambiguous/a/b v0.0.0-empty
-- b/b.go --
package b

<attribution xmlns:dc="http://purl.org/dc/elements/1.1/">
	<dc:creator>apeachyteach1</dc:creator>
	<dc:title>Ephemeral 2</dc:title>
	<dc:rights>https://creativecommons.org/licenses/by-nd/2.0/</dc:rights>
	<dc:identifier>https://www.flickr.com/photos/96967371@N03/9166833779</dc:identifier>
	<dc:type>StillImage</dc:type>
</attribution>
