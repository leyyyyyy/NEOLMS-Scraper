// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: red; icon-glyph: magic;
const widget = new ListWidget();

Script.setWidget(widget);
Script.complete();

const files = FileManager.iCloud();



var poop = new Request(API_URL)
poop.headers = {HEADERS}
var response = await poop.loadJSON()


var elementFont = new Font("AppleSDGothicNeo-Light", 13)
var subjectFont = new Font('AppleSDGothicNeo-Bold', 13)
var titleFont = new Font("Helvetica-BoldOblique", 20)
var title = widget.addText("ASSIGNMENTS");
title.font = titleFont
title.textColor = new Color("black", 1)
title.centerAlignText()

widget.addSpacer()
var assignCount = 0
var assignArray = []
for (let i = 0; i < response.length; i++) {
  for (let x = 0; x < response[i]["tasks"].length; x++) {
    dict = response[i]["tasks"][x]
    dict["subject"] = response[i]["subject"]
    assignArray.push(response[i]["tasks"][x])
    }
}



assignArray.sort((a,b)=> {return Date.parse(a.deadline) - Date.parse(b.deadline)})

for (let i = 0; i < assignArray.length; i++) {
  
  var dateObj
  
  if (i > 13){
    console.log('too much')
    var stack = widget.addStack();
    stack.addSpacer()
    text = stack.addText("...")
    text.font = elementFont
    text.textColor = new Color("black", 1)
    stack.addSpacer()
    break;
  }
  
  
  
  var stack = widget.addStack();
  console.log(assignArray[i]["task"])

 
  subj1 = stack.addText(" " + assignArray[i]["subject"])
  subj1.font = subjectFont
  subj1.textColor = new Color("black", 1)

  stack.addSpacer()

  assignmentName = assignArray[i]["task"]
  if (assignmentName.length > 22){
    assignmentName = assignmentName.substr(0, 22) + "..."
  }

  count = stack.addText(assignmentName);
  count.font = elementFont
  count.textColor = new Color("black", 1)


  stack.addSpacer()

  if ("deadline" in assignArray[i]){
    dateObj= new Date(assignArray[i].deadline)
    deadline= dateObj.toString().split(" ")
    time = deadline[4].split(":")
    if (deadline[4] == "23:59:00")
    {
    dl = stack.addText(" " + deadline[1]+ " " + deadline[2])
    }

    else {
      dl = stack.addText(" " + deadline[1]+ " " + deadline[2] + " " + time[0]+":"+time[1])
    }

    dl.font = subjectFont
    dl.textColor = new Color("black", 1)
    widget.addSpacer(3)
  } 
  else {
    dl = stack.addText("N/A")
    dl.font = subjectFont
    dl.textColor = new Color("black", 1)
    widget.addSpacer(3)
  }


}


widget.backgroundImage = files.readImage(files.bookmarkedPath("clear.jpg"))
widget.presentLarge()


