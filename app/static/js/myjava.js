// Tooltip only Text$(document).ready(function() {	$('.StoryDescription').hover(function(){			// Hover over code			var title = $(this).attr('title');			$(this).data('tipText', title).removeAttr('title');			$('<p class="ToolTip"></p>')			.text(title)			.appendTo('body')			.fadeIn('slow');	}, function() {			// Hover out code			$(this).attr('title', $(this).data('tipText'));			$('.ToolTip').remove();	}).mousemove(function(e) {			var mousex = e.pageX + 10; //Get X coordinates			var mousey = e.pageY + 10; //Get Y coordinates			$('.ToolTip')			.css({ top: mousey, left: mousex })	});});// $('input[class=AssumptionLink]').on('input', function(e) {//   var input = $(e.target),//       datalist = input.attr('data-list');////   if(input.val().length < 3) {//       input.attr('list', '');//   } else {//       input.attr('list', datalist);//   }// });// Function for going backfunction goBack() {	window.history.back();}// Function for searching user storiesfunction searchStories() {	var searchVar = document.getElementById("searchBox").value.toLowerCase();	if (searchVar == '') {		location.reload();	}	var stories = document.getElementsByClassName("StoryTitle");	var descriptions = document.getElementsByClassName("StoryDescription");	var titles = [];	var descripts = [];	var cellType = 1;	for (var i = 1; i < stories.length; i++) {		stories[i].parentElement.style.display = "";		titles[i] = stories[i].innerHTML.toLowerCase();		descripts[i] = descriptions[i].innerHTML.toLowerCase();		if (titles[i].indexOf(searchVar) >= 0 || descripts[i].indexOf(searchVar) >= 0) {			stories[i].parentElement.className = "TableRow Row" + (cellType % 2 + 1);			cellType++;			continue;		}		stories[i].parentElement.style.display = 'none';	}}// Keeping the buttons$(window).scroll(function () {	var $width = $(window).width();	$width = $width/2;	var $location = $width - 464;	if ($(window).scrollTop() > 150) {		$('.SearchContainer').attr("class", "NewSearchContainer");		$('.NewSearchContainer').css({'right': $location + 'px'});	}	if ($(window).scrollTop() < 150) {		$('.NewSearchContainer').attr("class", "SearchContainer");	}});// Making a popupfunction helpPopup(mylink, windowname) {  	var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left; 	var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top; 	var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width; 	var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height; 	var left = ((width / 2) - (900 / 2)) + dualScreenLeft; 	var top = ((height / 2) - (600 / 2)) + dualScreenTop;	if (! window.focus)return true;	var href;	if (typeof(mylink) == 'string') href=mylink;	else href=mylink.href; 	window.open(href, windowname, 'width=1000,height=500,scrollbars=yes,top=' + top + ', left=' + left);	return false; }// For alternating row stylesfunction addRows() {	var rows = document.getElementsByClassName("TableRow");	for (var i = 1; i < rows.length; i++) {		var rowNum = (i % 2) + 1;		rows[i].className += " Row" + rowNum;	}		// For using "enter" as search	document.getElementById("searchBox").addEventListener("keyup", function(event) {		event.preventDefault();		if (event.keyCode == 13) {			document.getElementById("searchButton").click();		}	});}// For adding Step number to walkthroughsfunction addStep() {	var container = document.getElementsByClassName("StoryWalkthrough");	var storyParas = document.getElementsByClassName("StoryParagraph");	var stepNum = 1;	for (var num = 0; num < storyParas.length; num++) {		var para = document.createElement("p");		para.className = "StoryStep";		if (num == 0) {			para.className += " StoryStep1";			var node = document.createTextNode("Step " + stepNum + ":");			para.appendChild(node);			container[0].insertBefore(para, storyParas[num]);			stepNum++;		}		else {			if (storyParas[num].innerText.charAt(0) != "(") {				node = document.createTextNode("Step " + stepNum + ":");				para.appendChild(node);				container[0].insertBefore(para, storyParas[num]);				stepNum++;			}			else if (storyParas[num].innerText.charAt(0) == "(") {				node = document.createTextNode("Note:");				para.style.fontWeight = "bolder";				para.appendChild(node);				container[0].insertBefore(para, storyParas[num]);			}		}	}}// For getting home pagefunction getHome() {	var params = window.location.search.substring(1);	params = params.split(",");	library = [];	for (var i = 0; i < params.length; i++) {		library[i] = params[i].split("=");	}	var homeType = library[0][1];	if (homeType == 1) {		location.href = "homeSS.html?page=1";	}	else if (homeType == 2) {		location.href = "homePO.html?page=2";	}	else if (homeType == 3) {		location.href = "homeOther.html?page=3";	}	else if (homeType == 4) {		location.href = "homeIndex.html?page=4";	}	else {		location.href = "index.html";	}}// For changing pagesfunction change(e, epic, lastEpic) {	var newWindow = false;	try {		var url = convertURL(e.children[0].children[0].innerText);	}	catch (err) {		try {			url = convertURL(e.children[0].innerText);			newWindow = true;		}		catch(err) {			alert("Sorry, this link is broken");			return;		}	}	if (epic) {		url = url + "epic";	}	url = url + ".html";	var params = window.location.search.substring(1);	lastEpic = "" + lastEpic;	if (lastEpic != "undefined") {		try {			location.href = url + "?" + params + ",epic=" + lastEpic;		}		catch (err) {			alert("Sorry, this link is broken");		}	}	else {		params = params.split(",");		if (newWindow) {			event.stopPropagation();			var win = window.open(url + "?5", '_blank');			win.focus();		}		else {			try {				location.href = url + "?" + params[0];			}			catch (err) {				alert("Sorry, this link is broken");			}		}	}}function convertURL(text) {	text = text.toLowerCase().replace(/ /g, "").replace(/\,/g, "").replace(/\//g, "");	return text;}function changeTo(e) {	location.href = e;}function change2(url) {	event.stopPropagation();	var win = window.open(url + "?5", '_blank');	win.focus();}// function loadEpics() {// 	var params = window.location.search.substring(1);// 	params = params.split(",");// 	var library = [];// 	for (var i = 0; i < params.length; i++) {// 		library[i] = params[i].split("=");// 	}// 	container = document.getElementsByClassName("Whole");// 	container = container[0];// 	secondChild = container.children[1];// 	if (library.length >= 2) {// 		epicContainer = document.createElement("DIV");// 		epicContainer.className = "StoryHolder";// 		epicHeader = document.createElement("P");// 		epicHeader.className = "StoryHeader EpicHeader";// 		epicHeader.innerHTML = "<b>Containing Epic(s)</b>";// 		epicTable = document.createElement("DIV");// 		epicTable.className = "StoryTable EpicTable";// 		epicContainer.appendChild(epicHeader);// 		epicContainer.appendChild(epicTable);// 		for (var i = 1; i < library.length; i++) {// 			var rowType = library.length - i;// 			epicRow = document.createElement("DIV");// 			epicRow.className = "TableHeaderRow StoryTableRow EpicRow Epic" + rowType;// 			var epicCell = document.createElement("DIV");// 			epicCell.className = "ContainingEpicTitle";//// 			var epicName = document.createTextNode(library[i][1].toUpperCase().replace(/%20/g, " "));// 			epicCell.appendChild(epicName);// 			epicTable.appendChild(epicRow);// 			epicRow.appendChild(epicCell);// 			var paramsToAdd = params[0];// 			for (var j = 1; j < i; j++) {// 				paramsToAdd += "," + params[j];// 			}// 			epicRow.onclick = createURL.bind(null, library[i][1], paramsToAdd);// 		}// 		container.insertBefore(epicContainer, secondChild);// 	}////////// 	flowContainer = document.createElement("DIV");// 	flowContainer.className = "StoryHolder";// 	flowHeader = document.createElement("P");// 	flowHeader.className = "StoryHeader EpicHeader Underlined WorkflowLink";// 	flowHeader.innerHTML = "See Workflow";// 	flowContainer.appendChild(flowHeader);// 	flowHeader.onclick = createURL.bind(null, "processflowexample.html", -1);// 	container.insertBefore(flowContainer, secondChild);// }function createURL(page, param) {	if (param != -1) {		page = page.replace(/%20/g, "");		page = page.replace(/ /g, "");		var url = page + "epic.html";		location.href = url + "?" + param;	}	else {		var value = window.location.pathname.split("/");		var oldURL = value[value.length - 1].split(".")[0];		var win = window.open(page + "?" + oldURL, '_blank');		win.focus();	}}function refreshPage() {	window.location.href = window.location.pathname;}//For Drag and Dropfunction allowDrop(ev) {    ev.preventDefault();}function drag(ev) {	ev.dataTransfer.setData("text", ev.target.id);}function drop(ev) {    ev.preventDefault();    var data = ev.dataTransfer.getData("text");	var container = document.getElementById("walkthroughAddBox");	var deletor = document.createElement("DIV");	deletor.className = "Delete";	deletor.innerHTML = "&#9986;";	deletor.addEventListener("click", function deleteThis() {		if (container.children.length > 5) {			container.removeChild(deletor.parentNode.previousSibling);			container.removeChild(deletor.parentNode);		}		else {			step.value = "";		}	});	if (data.includes("stepLine")) {		var oldStep = document.getElementById(data);		if (ev.target.nextSibling == oldStep) {			return		}		else {			var dragLine = oldStep.previousElementSibling;			container.insertBefore(dragLine, ev.target.nextElementSibling);			container.insertBefore(oldStep, dragLine);		}		return;	}	var step;	step = document.createElement("INPUT");	if (data == "stepDrag") {		step.className = "AddInput Step";		step.type = "text";		step.setAttribute("autocomplete", "off");		step.setAttribute("placeholder", "Step");	}	else if (data == "noteDrag") {		step.className = "AddInput Note";		step.type = "text";		step.setAttribute("autocomplete", "off");		step.setAttribute("placeholder", "Note");	}	else if (data == "imageDrag") {		step.className = "AddInput ImageInput";		step.type = "File";	}	var dragLine = document.createElement("DIV");	dragLine.className = "StepLine Between DragStepLine";	dragLine.setAttribute("ondragover", "allowDrop(event)");	dragLine.setAttribute("ondrop", "drop(event)");	step.id = "step" + ((container.children.length - 1)/2);	step.name = "step";	var line = document.createElement("DIV");	line.className = "StepLine";	line.id = "stepLine" + ((container.children.length - 1)/2);	line.setAttribute("draggable", "true");	line.setAttribute("ondragstart", "drag(event)");	container.insertBefore(line, ev.target.parentNode);	container.insertBefore(dragLine, line);	line.appendChild(deletor);	line.appendChild(step);}// For zooming in on a process cellfunction zoomIn(e) {	var block = document.getElementById("blocker");	block.style.zIndex = 1000;	var height = computeHeight(e);	var width = computeWidth(e);		if (e.style.width == "") {		e.style.height = height + 15 + "px";		e.style.width = width + "px";		var innerCells = e.children;		var biggestChild = width;		for (var i = 1; i < e.parentElement.children.length; i++) {			if (e.parentElement.children[i].clientWidth > biggestChild) {				biggestChild = e.parentElement.children[i].clientWidth;			}		}		while(e.parentElement.className != "SearchContainer LifeProcessWhole") {			for (i = 1; i < e.parentElement.children.length; i++) {				if (e.parentElement.children[i].clientWidth > biggestChild) {					biggestChild = e.parentElement.children[i].clientWidth;				}			}			var ph = height + e.parentElement.clientHeight;			var double = (e.classList[1] == "Double");			if (double) {				biggestChild = e.parentElement.clientWidth;			}			var pw = biggestChild + 30;			e.parentElement.style.height = ph + "px";			e.parentElement.style.width = pw + "px";			try {				if (e.nextElementSibling.classList[1] == "AfterDouble") {					e.nextElementSibling.style.height = e.nextElementSibling.clientHeight + height + "px";				}				if (e.nextElementSibling.nextElementSibling.nextElementSibling.classList[1] == "AfterDouble") {					e.nextElementSibling.nextElementSibling.nextElementSibling.style.height = e.nextElementSibling.nextElementSibling.nextElementSibling.clientHeight + height + "px";				}			}			catch (err) {}			e = e.parentNode;			biggestChild += 30;		}		event.stopPropagation();		setTimeout(function() {			for (var i = 0; i < innerCells.length; i++) {				if (e.style.height != "") {					innerCells[i].classList.remove("Hidden");				}			}		}, 500);	}	else {		e.style.height = "";		e.style.width = "";		height = e.clientHeight - 15;		innerCells = e.getElementsByClassName("Inner");		for (i = 0; i < innerCells.length; i++) {			innerCells[i].classList.add("Hidden");			innerCells[i].style.height = "";			innerCells[i].style.width = "";		}		biggestChild = 180;		for (i = 1; i < e.parentElement.children.length; i++) {			if (parseInt(e.parentElement.children[i].style.width) >= biggestChild) {				biggestChild = e.parentElement.children[i].clientWidth + 30;			}		}		while(e.parentElement.className != "SearchContainer LifeProcessWhole") {			for (i = 1; i < e.parentElement.children.length; i++) {				if (e.parentElement.children[i] != e) {					if (parseInt(e.parentElement.children[i].style.width) >= biggestChild) {						biggestChild = e.parentElement.children[i].clientWidth + 30;					}				}			}			ph = e.parentElement.clientHeight - height;			double = (e.classList[1] == "Double");			if (double) {				biggestChild = e.parentElement.clientWidth - 30;			}			pw = biggestChild;			e.parentElement.style.height = ph + "px";			e.parentElement.style.width = pw + "px";			try {				if (e.nextElementSibling.classList[1] == "AfterDouble") {					e.nextElementSibling.style.height = "";				}				if (e.nextElementSibling.nextElementSibling.nextElementSibling.classList[1] == "AfterDouble") {					e.nextElementSibling.nextElementSibling.nextElementSibling.style.height = "";				}			}			catch (err) {}			e = e.parentNode;			biggestChild += 30;		}		event.stopPropagation();	}	setTimeout(function() {		block.style.zIndex = "";	}, 500);}function computeHeight(e) {	var innerCells = e.children;	var height = 0;	for (var i = 0; i < innerCells.length; i++) {		height += 42;		if (innerCells[i].classList[1] == "Double") {			i += 2;		}		if (innerCells[i].classList[1] == "AfterDouble") {			height += 20;		}	}	return height;}function computeWidth(e) {	var thisClass = 0;	if (e.children.length > 1 ) {		thisClass = e.children[1].classList[1];	}	if (thisClass == "Double") {		return 430;	}	else if (thisClass == "Single" || thisClass == 0) {		return 180;	}}// For opening process cells to the appropriate cellfunction expandTo() {	var container = document.getElementsByClassName("SearchContainer")[0];	var names = document.getElementsByClassName("ProcessHeader");	var text = [];	for (var i = 0; i < names.length; i++) {		text[i] = names[i].innerText;	}	var desiredCell = window.location.search.substring(1);	if (desiredCell != "") {		if (desiredCell.substring(desiredCell.length - 4) == "epic") {			desiredCell = desiredCell.substring(0, desiredCell.length - 4);		}		for (i = 0; i < text.length; i++) {			var cell = text[i].toLowerCase().replace(/ /g, "").replace(/\//g, "");			if (desiredCell.toLowerCase() == cell) {				var toClick = [];				var e = names[i].parentElement;								while(e.parentElement.className != "SearchContainer LifeProcessWhole") {					toClick.push(e.parentElement);					e = e.parentElement;				}				for (var j = toClick.length - 1; j >= 0; j--) {					toClick[j].classList.add("NoTransition");				}				for (j = toClick.length - 1; j >= 0; j--) {					expand(toClick[j]);				}				for (j = toClick.length - 1; j >= 0; j--) {					toClick[j].classList.remove("NoTransition");				}				/*names[i].scrollIntoView(false);*/				setTimeout(function() {					container.scrollTop = names[i].getBoundingClientRect().top - 100;				}, 5);				setTimeout(function(){					names[i].parentElement.style.background = "#AAB361";					names[i].parentElement.style.color = "white";					setTimeout(function(){						names[i].parentElement.style.background = "";	  					names[i].parentElement.style.color = "";					}, 800);				}, 1000);				break;			}		}	}}function expand(e) {	var height = computeHeight(e);	var width = computeWidth(e);	e.style.height = height + 15 + "px";	e.style.width = width + "px";	var innerCells = e.children;	var biggestChild = width;	for (var i = 1; i < e.parentElement.children.length; i++) {		if (e.parentElement.children[i].clientWidth > biggestChild) {			biggestChild = e.parentElement.children[i].clientWidth;		}	}	while(e.parentElement.className != "SearchContainer LifeProcessWhole") {		for (i = 1; i < e.parentElement.children.length; i++) {			if (e.parentElement.children[i].clientWidth > biggestChild) {				biggestChild = e.parentElement.children[i].clientWidth;			}		}		var ph = height + e.parentElement.clientHeight;		var double = (e.classList[1] == "Double");		if (double) {			biggestChild = e.parentElement.clientWidth;		}		var pw = biggestChild + 30;		e.parentElement.style.height = ph + "px";		e.parentElement.style.width = pw + "px";		e = e.parentNode;		biggestChild += 30;	}	event.stopPropagation();	for (i = 0; i < innerCells.length; i++) {			innerCells[i].classList.remove("Hidden");		}}function addWalkthroughStep(button) {	var selector = button.id;	var container = document.getElementById("walkthroughAddBox");	var buttonContainer = document.getElementsByClassName("LastStepLine")[0];	var step;	step = document.createElement("INPUT");	if (selector == "stepButton") {		step.className = "AddInput Step";		step.type = "text";		step.setAttribute("autocomplete", "off");		step.setAttribute("placeholder", "Step");	}	else if (selector == "noteButton") {		step.className = "AddInput Note";		step.type = "text";		step.setAttribute("autocomplete", "off");		step.setAttribute("placeholder", "Note");	}	else if (selector == "imageButton") {		step.className = "AddInput ImageInput";		step.type = "File";	}	step.id = "step" + (container.children.length);	step.name = "step";	var deletor = document.createElement("DIV");	deletor.className = "Delete";	deletor.innerHTML = "&#9986;";	deletor.addEventListener("click", function deleteThis() {		if (container.children.length > 2) {			container.removeChild(deletor.parentNode.previousSibling);            container.removeChild(deletor.parentNode);        }        else {			step.value = "";		}	});	var line = document.createElement("DIV");	line.className = "StepLine";	var dragLine = document.createElement("DIV");	dragLine.className = "StepLine Between DragStepLine";	dragLine.setAttribute("ondragover", "allowDrop(event)");	dragLine.setAttribute("ondrop", "drop(event)");	step.id = "step" + ((container.children.length)/2);	line.id = "stepLine" + ((container.children.length)/2);	line.setAttribute("draggable", "true");	line.setAttribute("ondragstart", "drag(event)");	container.insertBefore(dragLine, buttonContainer);	container.insertBefore(line, buttonContainer);	line.appendChild(deletor);	line.appendChild(step);	if (step.className != "AddInput ImageInput") {		step.focus();	}}function showList(e) {	if (e.value.length > 1) {		if (e.className == "AssumptionLink") {			e.setAttribute("list", "storyList");		}		if (e.className == "AddInput EpicInput") {			e.setAttribute("list", "epicList");		}	}	if (e.value.length < 1) {		e.setAttribute("list", "");	}}function addStoryAssumption() {	var container = document.getElementById("assumptionBox");	var button = document.getElementById("addAssumption");	var assumption = document.createElement("INPUT");	assumption.className = "AddInput AssumptionInput";	var link = document.createElement("INPUT");	link.className = "AssumptionLink";	assumption.name = "assumption";	link.name = "assumption_link";	assumption.setAttribute("autocomplete", "off");	link.setAttribute("oninput", "showList(this);");	link.setAttribute("autocomplete", "off");	link.style.marginLeft = "8px";	var deletor = document.createElement("DIV");	deletor.className = "Delete DeleteAssumption";	deletor.innerHTML = "&#9986;";	deletor.addEventListener("click", function deleteThis() {		if (container.children.length > 4) {            container.removeChild(deletor.parentNode);        }        else {			assumption.value = "";			link.value = "";		}	});	var line = document.createElement("DIV");	line.className = "AssumptionLine";	container.insertBefore(line, button);	line.appendChild(deletor);	line.appendChild(assumption);	line.appendChild(link);}function checkForm() {	var title = document.getElementsByName("title")[0];	var description = document.getElementsByName("description")[0];	var assumptions = document.getElementsByClassName("AssumptionInput");	var links = document.getElementsByClassName("AssumptionLink");	if (title.value == '') {		alert("Please enter a Title");		return false;	}	if (description.value == '') {		alert("Please enter a Description");		return false;	}	for (var i = 0; i < assumptions.length; i++) {		if (assumptions[i].value == '' && links[i].value != '') {			alert("Please enter an assumption for story '" + links[i].value + "'");			return false;		}	}	var steps = document.getElementsByClassName("ImageInput");	var container = document.getElementById("walkthroughAddBox");	if (steps.length > 0) {		for (i = 0; i < steps.length; i++) {			var path = steps[i].value.split("\\");			path = path[path.length - 1];			var newStep = document.createElement("INPUT");			newStep.className = "AddInput NewImage";			newStep.type = "text";			newStep.id = steps[i].id;			newStep.name = "step";			newStep.value = path;			steps[i].parentNode.insertBefore(newStep, steps[i]);			steps[i].style.display = 'none';		}	}	var notes = document.getElementsByClassName("Note");	if (notes.length > 0) {		for (i = 0; i < notes.length; i++) {			var content = notes[i].value;			content = "(" + content + ")";			// content = content.replace(/'/g, "&#39");			// content = content.replace(/\"/g, "&#34");			notes[i].value = encodeURIComponent(content);		}	}	steps = document.getElementsByClassName("Step");	for (i = 0; i < steps.length; i++) {		// steps[i].value = steps[i].value.replace(/'/g, "&#39");		// steps[i].value = steps[i].value.replace(/\"/g, "&#34");		steps[i].value = encodeURIComponent(steps[i].value);	}	var form = document.getElementById("storyForm");	var params = window.location.search.substring(1).split("&");	if (params.length > 1) {		var edit = params[1].split("=")[1];		if (edit) {			form.setAttribute("action", form.getAttribute("action") + "?" + params.join("&"));		}	}	return true;}function decodeSteps() {	var steps = document.getElementsByClassName("StoryParagraph");	if (steps.length > 0) {        for (var i = 0; i < steps.length; i++) {            steps[i].innerHTML = decodeURIComponent(steps[i].innerHTML);        }    }	steps = document.getElementsByClassName("Step");	if (steps.length > 0) {        for (i = 0; i < steps.length; i++) {            steps[i].value = decodeURIComponent(steps[i].value);            // steps[i].value = steps[i].value.replace(/&#39/g, "'");			// steps[i].value = steps[i].value.replace(/&#34/g, "\"");            if (steps[i].value.charAt(0) == "(") {            	steps[i].value = steps[i].value.slice(1, steps[i].value.length - 1);            	steps[i].className = "AddInput Note";            	i--;			}        }    }    var images = document.getElementsByClassName("StoryImage");	if (images.length > 0) {		for (i = 0; i < images.length; i++) {			var oldSource = images[i].getAttribute("src");			var newSource = decodeURIComponent(oldSource);			images[i].setAttribute("src", newSource);		}	}}function checkFlash() {	var flashes = document.getElementsByClassName("FlashMessages");	if (flashes.length > 0) {		flashes = flashes[0];		flashes.style.opacity = "1";		setTimeout(function() {			flashes.style.opacity = "0";		}, 1500);		setTimeout(function() {			flashes.style.display = "none";		}, 2500);	}}/* For adding arrow image */function addImage() {	var container = document.getElementsByClassName("StoryWalkthrough")[0];	var arrow = document.createElement("IMG");	var newLine = document.createElement("BR");	arrow.className = "ArrowDown";	arrow.setAttribute("src", "static/images/template/arrow_down.gif");	for (var i = 1; i < container.children.length; i++) {		if (container.children[i].className == "StoryImage" && container.children[i + 1].className == "StoryImage") {			container.insertBefore(newLine.cloneNode(true), container.children[i + 1]);			i++;			container.insertBefore(arrow.cloneNode(true), container.children[i + 1]);			i++;		}	}}function deleteStep(deletor) {	if (deletor.parentNode.parentNode.children.length > 6) {        deletor.parentNode.parentNode.removeChild(deletor.parentNode.previousElementSibling);        deletor.parentNode.parentNode.removeChild(deletor.parentNode);    }    else {		deletor.nextElementSibling.value = "";	}}function deleteAssumption(deletor) {	if (deletor.parentNode.parentNode.children.length > 4) {        deletor.parentNode.parentNode.removeChild(deletor.parentNode);    }    else {		deletor.nextElementSibling.value = "";		deletor.nextElementSibling.nextElementSibling.value = "";	}}function CheckDelete() {	return confirm("Are you sure you want to delete this story?");}