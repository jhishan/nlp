var express = require('express');
var router = express.Router();
var atob = require('atob');
var afinn = require('../afinn.json');
var Snowball = require('snowball');
var stemmer = new Snowball('English');

allMessages = [];

/*
google api stuff.

A lot of the standard code for connecting is taking
right from developer site. I did not write any of it. 

I will label the code that is actually a part of my project
*/
var fs = require('fs');
var readline = require('readline');
var google = require('googleapis');
var googleAuth = require('google-auth-library');

// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/gmail-nodejs-quickstart.json
var SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];
var TOKEN_DIR = (process.env.HOME || process.env.HOMEPATH ||
	process.env.USERPROFILE) + '/.credentials/';
var TOKEN_PATH = TOKEN_DIR + 'gmail-nodejs-quickstart.json';

// Load client secrets from a local file.
fs.readFile('client_secret.json', function processClientSecrets(err, content) {
	if (err) {
		console.log('Error loading client secret file: ' + err);
		return;
	}
	// Authorize a client with the loaded credentials, then call the
	// Gmail API.
	authorize(JSON.parse(content), getAllEmails);
});

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 *
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, callback) {
	var clientSecret = credentials.installed.client_secret;
	var clientId = credentials.installed.client_id;
	var redirectUrl = credentials.installed.redirect_uris[0];
	var auth = new googleAuth();
	var oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl);

	// Check if we have previously stored a token.
	fs.readFile(TOKEN_PATH, function(err, token) {
		if (err) {
			getNewToken(oauth2Client, callback);
		} else {
			oauth2Client.credentials = JSON.parse(token);
			callback(oauth2Client);
		}
	});
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 *
 * @param {google.auth.OAuth2} oauth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback to call with the authorized
 *     client.
 */
function getNewToken(oauth2Client, callback) {
	var authUrl = oauth2Client.generateAuthUrl({
		access_type: 'offline',
		scope: SCOPES
	});
	console.log('Authorize this app by visiting this url: ', authUrl);
	var rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout
	});
	rl.question('Enter the code from that page here: ', function(code) {
		rl.close();
		oauth2Client.getToken(code, function(err, token) {
			if (err) {
				console.log('Error while trying to retrieve access token', err);
				return;
			}
			oauth2Client.credentials = token;
			storeToken(token);
			callback(oauth2Client);
		});
	});
}

/**
 * Store token to disk be used in later program executions.
 *
 * @param {Object} token The token to store to disk.
 */
function storeToken(token) {
	try {
		fs.mkdirSync(TOKEN_DIR);
	} catch (err) {
		if (err.code != 'EEXIST') {
			throw err;
		}
	}
	fs.writeFile(TOKEN_PATH, JSON.stringify(token));
	console.log('Token stored to ' + TOKEN_PATH);
}

function getAllEmails(auth) {
	var gmail = google.gmail('v1');
	gmail.users.messages.list({
		auth: auth,
		userId: 'me',
	}, function(err, response){
		if(err){
			console.log("error occured");
			return;
		}
		var messageList = response.messages;
				
		messageList.forEach(function(message){
			var messageId = message.id;
			getMessage(messageId);
			function getMessage(messageId) {
				var request = gmail.users.messages.get({
					auth: auth,
					'userId': 'me',
					'id': messageId
				}, function(err, response){
					if(response.payload.parts != undefined){
						if(response.payload.parts[0].body.data != undefined){
							var emailBodyText = atob(response.payload.parts[0].body.data.toString());
							var isHTMLEmail = false;
							var currentEmailObject = {};
							if(emailBodyText.indexOf('<') > -1 && emailBodyText.indexOf('>') > -1){
								isHTMLEmail = true;
							}
							if(!isHTMLEmail){
								var emailSubject = '';
								response.payload.headers.forEach(function(header){
									if(header.name == 'Subject'){
										emailSubject = header.value;
									} 
								});
								
								if(emailSubject.length > 0){
									var emailBodyArray = emailBodyText.toLowerCase().split(" ");
									var count = 0;
									emailBodyArray.forEach(function(word){
										if(afinn.hasOwnProperty(word)){
											count += afinn[word];
										}else{
											stemmer.setCurrent(word);
											stemmer.stem();
											var stemmedWord = stemmer.getCurrent();
											if(afinn.hasOwnProperty(stemmedWord)){
												count += afinn[stemmedWord];
												/*
												console.log("original word is " + word);
												console.log("stem is " + stemmedWord);
												console.log();
												*/	
											}
										}
									});
									
									if(emailBodyText.length > 2000){
										emailBodyText = emailBodyText.substring(0, 2000);
										emailBodyText = emailBodyText + " ..."
									}		
								
									currentEmailObject['subject'] = emailSubject;
									currentEmailObject['body'] = emailBodyText;
									currentEmailObject['timestamp'] = parseInt(response.internalDate);
									currentEmailObject['sentimentNumber'] = count;
									//DO THE SENTIMENT ANALYSIS, CHECK STEMMING
									allMessages.push(currentEmailObject);
								}
							}
								
						}
					}                    
				});
			}
		});
		  
	});
}

/* GET home page. */
router.get('/', function(req, res, next) {
	sorted = allMessages.sort(function(messageOne, messageTwo){
    	return messageTwo.timestamp - messageOne.timestamp;
	});
	res.render('index', {messages: sorted});
});

module.exports = router;