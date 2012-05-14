var bgColorArray = [getRandomInt(100,150),getRandomInt(100,150),getRandomInt(100,150)];
var branchColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
var leafColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
var targetWord;

function fakeRefreshingColors(){
	bgColorArray = [getRandomInt(100,150),getRandomInt(100,150),getRandomInt(100,150)];
	branchColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
	leafColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
	
}

function colorTreeWithoutAPI(mode){
	if (mode == 'reset'){
		bgColorArray = [getRandomInt(100,150),getRandomInt(100,150),getRandomInt(100,150)];
		branchColorArray = [bgColorArray[0],bgColorArray[1],bgColorArray[2]];
		leafColorArray = [bgColorArray[0],bgColorArray[1],bgColorArray[2]];
	}
	if (mode == 'apiCallFailure'){
		bgColorArray = [getRandomInt(100,150),getRandomInt(100,150),getRandomInt(100,150)];
		branchColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
		leafColorArray = [getRandomInt(0,255),getRandomInt(0,255),getRandomInt(0,255)];
	}
}

function colorTreeWithAPICallData(hue,saturation,value){
	leafColorArray = [parseInt(hue.split(',')[0]), parseInt(hue.split(',')[1]),parseInt(hue.split(',')[2])];
	branchColorArray = [parseInt(saturation.split(',')[0]), parseInt(saturation.split(',')[1]),parseInt(saturation.split(',')[2])];
	bgColorArray = [parseInt(value.split(',')[0]), parseInt(value.split(',')[1]),parseInt(value.split(',')[2])];	
	reDrawTree();
	console.log("hue is " + hue);
	console.log("saturation is " + saturation);
	console.log("value is " + value);
	
}


function getRandomInt(min, max)
{
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function moveToView(targetView){
	
	 if (targetView == "results"){
	 $('div#wordinputpanel').css('position','absolute');
	 $('div#wordinputpanel').css('left', '-100%');
	
	 $('div#resultpanel').css('position','relative');
	 $('div#resultpanel').css('left', '0%');
	}
	
	if (targetView == "mainForm"){
		 $('div#wordinputpanel').css('position','relative');
		 $('div#wordinputpanel').css('left', '0%');

		 $('div#resultpanel').css('position','absolute');
		 $('div#resultpanel').css('left', '-100%');
	}
	
}

function setActiveResultsMarkup(mode){
	if (mode == "makingAPICall"){
		 $("div#loadingIndicator").css("display","block");
		 $("div#robotoWorking").css("display","block");
		 $("div#robotoFailure").css("display","none");		 
		 $("div#robotoSuccessful").css("display","none");		
	}
	if (mode == "apiCallSuccess"){
		 $("div#robotoWorking").css("display","none");
		 $("div#loadingIndicator").css("display","none");
		 $("div#robotoFailure").css("display","none");		 
		 $("div#robotoSuccessful").css("display","block");
	}
	if (mode == "apiCallFailure"){
		$("div#robotoWorking").css("display","none");
		$("div#loadingIndicator").css("display","none");
		$("div#robotoSuccessful").css("display","none");			
		$("div#robotoFailure").css("display","block");		
	}
}

function getTargetWord(){

	 targetWord = $('input#targetWord').val();
	 $('span#targetWord').text(targetWord);
	 $('input#targetWord').val("");	
	
}

function queryAPI(){
	
	var urlToCall = '/api';
	
	if (targetWord == 'lasagna'){
		urlToCall = '/lasagna';
	}
	
	$.ajax({
   		type: 'GET',
   		url: urlToCall, // or your absolute-path
   		data : {'word':targetWord},
   		dataType : 'json',
   		success : function(resp) 
             {
             console.info("Ajax call to color of words API succeeded");
             console.log(resp);
			 $("a#flickrLink").attr('href',resp.publicFlickrURL) //updating flickr link to this specific image word
			 setActiveResultsMarkup("apiCallSuccess");
			 colorTreeWithAPICallData(resp.hue,resp.saturation,resp.value);			 
             },
		error : function(jqXHR,textStatus,errorThrown){
			console.info("Ajax call to color of words API failed");
			console.log(textStatus);
			console.log(errorThrown);
			setActiveResultsMarkup("apiCallFailure");
			colorTreeWithoutAPI("apiCallFailure");
			reDrawTree();
			
		}
   });
	
}

function reDrawTree(){
	processingInstance = Processing.instances[0];  //variable allow processing functions to be called via js
	processingInstance.redraw();
}


$(document).ready(function() {
	
	//handling enter on the main form submit button
	$('form#wordinput').submit(function() {
      colorTreeWithoutAPI('reset');
      reDrawTree();
	  setActiveResultsMarkup('makingAPICall');
	  moveToView("results");
	  getTargetWord();
	  queryAPI();
	  return false;
	});
	

	//submitting main form via button click
	$("p#findColorButton").click(function() {
	
      colorTreeWithoutAPI('reset');
      reDrawTree();
	  setActiveResultsMarkup('makingAPICall');
	  moveToView("results");
	  getTargetWord();
	  queryAPI();
		
	});

	$("p#exploreAnotherButton").click(function() {

		 moveToView("mainForm");
		 colorTreeWithoutAPI('reset');
		 setActiveResultsMarkup('makingAPICall');
		 reDrawTree();

	   });	

	$("p#reGenerateButton").click(function() {
		reDrawTree();
		
	   });
	

});