function count (textArea){
const maxNumOfChars=textArea.getAttribute("maxlength");
$('textarea').keyup(function(){
    var currentLength=$(this).val().length;
    var remainingLength=maxNumOfChars-currentLength;
    $('#char_count').text(emainingLength+"/"+maxNumOfChars)
})
//const currentLength=textArea.value.length;
/*const remainingLength=maxNumOfChars-currentLength;
const characterCounter=textArea.nextElementSiibling;
characterCounter.textContent=remainingLength+"/"+maxNumOfChars
if (counter<0){
    characterCounter.style.color="red";

}else if (counter<20){
    characterCounter.style.color="orange";
}else{
    characterCounter.style.color="black";*/
}
