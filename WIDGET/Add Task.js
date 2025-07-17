// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: light-gray; icon-glyph: magic;


alert = new Alert("Add task")
alert.message = "Add task"
alert.addTextField("task name", "")

alert.addDestructiveAction("Cancel")
alert.addAction("Add")
alertIndex = await alert.present()
console.log(alert.textFieldValue())
if (alertIndex==1){
  var poop = new Request(API_URL)
poop.headers = {"taskName": alert.textFieldValue()}
var response = await poop.loadJSON()
}
  


