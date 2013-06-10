var phantom = require('phantom'),
	async = require('async');

function Pandora (username, password) {
	var self = this;

	self.login = function (fn) {
		self.page.open("http://www.pandora.com/account/sign-in", function (status) {
			setTimeout(function () {
				self.page.evaluate(function () {
					return $(".signinContainer").html();
				}, function (result) {
					console.log(result);
				});
			}, 5000);
		});

		function evaluator () {
			var email = $(".signinForm form input[name='email']"),
				pw = $(".signinForm form input[name='password']");
			setVal(email, 'sitpomk@gmail.com');
			setVal(pw, 'hello');

			$(".signinForm form input[name='email']").val('sitpomk :)');

			return $(".signinForm form input[name='email']").val();

			function setVal (el, val) {
				el.focus();
				el.val(val);
				el.trigger('keyUp keyPressed');
			}
		}

		function evalHandler (result) {
			fn(null, result);
		}
	};

	self.scrapeLikes = function (fn) {
		self.page.open("http://www.pandora.com/profile/likes/sitpomk", function (status) {
			setTimeout(function () {
				self.page.evaluate(function () {
					// return _.map($("#track_like_pages .section.clearfix .infobox h3"), function (e) { return $(e).text(); });
					return $("#track_like_pages").html();
				}, function (result) {
					console.log(result);
				});
			}, 5000);
		});
	};
}

exports.fetchTracks = function (username, password, fn) {
	var pandora = new Pandora(username, password);
	phantom.create(function (ph) {
		ph.createPage(function (page) {
			page.set('settings.userAgent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17');
			pandora.page = page;
			// Series of actions to perform on the page
			async.waterfall([
				pandora.scrapeLikes
			], function (err, result) {
				ph.exit();
				fn(result);
			});
		});
	});
};