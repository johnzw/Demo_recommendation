

function waterful(parent,out_box){
	//get all the box
	var oParent=document.getElementById(parent);
	var oBoxs = getByClass(oParent,out_box);
	//console.log(oBoxs.length);
	//get the width
	var oBoxsW=oBoxs[0].offsetWidth;
	var cols = Math.floor(document.documentElement.clientWidth/oBoxsW);
	//set width of main
	oParent.style.cssText='width:'+oBoxsW*cols+'px;margin:0 auto';
	
	var hArr = [];
	for(var i=0;i<oBoxs.length;i++){
		if(i<cols){
			hArr.push(oBoxs[i].offsetHeight);
		}
		else{
			var minH=Math.min.apply(null, hArr);
			var index = getMinhIndex(hArr,minH);
			oBoxs[i].style.position='absolute';
			oBoxs[i].style.top=minH+'px';
			oBoxs[i].style.left=oBoxsW*index+'px';
			//change the height
			hArr[index]+=oBoxs[i].offsetHeight;
		}
	}
}

//get element 
function getByClass(parent, clsName){
	var boxArr=new Array(); //get all the boxs
		oElements = parent.getElementsByTagName('*');
	
	for(var i=0;i<oElements.length;i++){
		if (oElements[i].className==clsName) {
			boxArr.push(oElements[i]);
		}
	}

	return boxArr;
}

//get min get
function getMinhIndex(arr, val){
	for(var i in arr){
		if(arr[i]==val){
			return i;
		}
	}
}

//check if it is okay to reload
function checkScrollSlide(){
	var oParent = document.getElementById('main');
	var oBoxs = getByClass(oParent,'out_box');
	var lastBoxH = oBoxs[oBoxs.length-1].offsetTop+Math.floor(oBoxs[oBoxs.length-1].offsetHeight/1.1)
	var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
	var height = document.body.clientHeight || document.documentElement.clientHeight
	return (lastBoxH<(scrollTop+height))?true:false;
}