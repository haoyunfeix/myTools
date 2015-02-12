#!/bin/sh
#
referer="$HTTP_REFERER"
echo "Content-type: text/html"
echo
form='<!doctype html>
<html>
	<head>
		<title>history.pushState/replaceState and referer headers</title>
	</head>
	<body>

		<noscript><p>Enable JavaScript and reload</p></noscript>
		<div id="log"></div>
		<script type="text/javascript">
var pyreferer = "'
echo "$form$referer\";"
echo 'var httpReferer = unescape(pyreferer);
var lastUrl = location.href.replace(/\/[^\/]*$/,"\/009-2.html?1234");
parent.test(function () {
	parent.assert_equals( httpReferer, lastUrl );
}, "HTTP Referer should use the pushed state");
parent.test(function () {
	parent.assert_equals( document.referrer, lastUrl );
}, "document.referrer should use the pushed state");
window.onload = function () {
	setTimeout(function () {
		try { history.pushState("","","009-4.html?2345"); } catch(e) {}
		location.href = "009-5.cgi";
	},10);
};
		</script>

	</body>
</html>'