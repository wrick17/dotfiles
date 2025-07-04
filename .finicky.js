// Link to Documentation: https://github.com/johnste/finicky/wiki/Configuration-(v4)

const urls = [
	"github.com/Sequoia-Engineering/*",
	"*.atlassian.net/*",
	"statics.teams.cdn.office.net/*",
	"jenkins-qa.sequoia-development.com/*",
	"jenkins-production.sequoia-development.com/*",
	"myapps.microsoft.com/*",
	"sonar-qa.sequoia-development.com/*",
	"sequoiaconsulting.zoom.us/*",
	"murren.greythr.com/*",
	"app.datadoghq.com/*",
	"app.aptrinsic.com/*",
	"itx.sequoia.com/*",
	"sequoiaone.sharepoint.com/*",
];

export default {
	defaultBrowser: "Orc",
	options: {
		checkForUpdates: false,
		logRequests: false,
	},
	handlers: urls.map((url) => ({
		match: url,
		browser: "Island",
	})),

	rewrite: [
		{
			match: "statics.teams.cdn.office.net/*",
			url: (url) => {
				const newUrl = decodeURIComponent(
					url.search.replace("?url=", ""),
				).split("&locale=en-us&dest=https://teams.microsoft.com")[0];
				return newUrl;
			},
		},
	],
};
