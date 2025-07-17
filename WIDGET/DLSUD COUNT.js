// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: green; icon-glyph: magic;
const widget = new ListWidget();

Script.setWidget(widget);
Script.complete();

const files = FileManager.iCloud();

console.log(files.fileExists(files.joinPath(files.documentsDirectory(), "image.jpg")))

var request = new Request(API_URL)
request.headers = {}
var response = await request.loadJSON()// 
// widget.addText(response[0]['subject'])
// widget.addText(response[0]['count'])
console.log(response)

var headline = new Font('AppleSDGothicNeo-Bold', 15)
var elementFont = new Font("AppleSDGothicNeo-Light", 15)

widget.addSpacer()


for (let i = 0; i < response.length; i++) {

if (i > 5){
  var stack = widget.addStack();
  text = stack.addText("...")
  text.font = headline
  text.textColor = new Color("black", 1)
  break
}
var stack = widget.addStack();
subj1 = stack.addText(response[i]['subject'])
subj1.font = headline
subj1.textColor = new Color("black", 1)
stack.addSpacer()

count = stack.addText(response[i]['count'].toString());

count.font = elementFont
count.textColor = new Color("black", 1)
stack.topAlignContent()

}
// stack.setPadding(0, 0, 0, 20)


widget.backgroundImage = files.readImage(files.joinPath(files.documentsDirectory(), "small clear.jpg"))
widget.presentSmall()


