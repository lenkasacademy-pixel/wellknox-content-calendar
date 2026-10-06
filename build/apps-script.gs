// Wellknox October 2026 shoot status API, bound to the sheet "Wellknox Oct 2026 shoots".
// Columns: A shoot_id, B place, C date, D status (planned or done), E updated_at.
var SEED = [
  ["shoot_id", "place", "date", "status", "updated_at"],
  ["s-hitech", "Hi-Tech City", "2026-10-09", "planned", ""],
  ["s-kukatpally", "Kukatpally", "2026-10-12", "planned", ""]
];

var SHEET_ID = "1uQhY5uvvJCKTgKXeu-HerCdRKexEs6vFkZwyrBIz524";

function sheet_() {
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
  if (sh.getLastRow() < 1) {
    sh.setName("Shoots");
    sh.getRange(1, 1, SEED.length, 5).setValues(SEED);
    sh.getRange(2, 3, SEED.length - 1, 1).setNumberFormat("@");
    sh.getRange(2, 3, SEED.length - 1, 1).setValues(SEED.slice(1).map(function (r) { return [r[2]]; }));
    sh.getRange(1, 1, 1, 5).setFontWeight("bold");
    sh.setFrozenRows(1);
    sh.autoResizeColumns(1, 5);
  }
  return sh;
}

function setup() { sheet_(); }

function read_() {
  var v = sheet_().getDataRange().getValues(), out = [];
  for (var i = 1; i < v.length; i++) {
    if (!v[i][0]) continue;
    var at = v[i][4];
    out.push({
      id: String(v[i][0]),
      status: String(v[i][3] || "planned"),
      at: at instanceof Date ? at.toISOString() : (at ? String(at) : "")
    });
  }
  return out;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() { return json_({ ok: true, shoots: read_() }); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var b = JSON.parse(e.postData.contents);
    if (b.status !== "done" && b.status !== "planned") return json_({ ok: false, error: "bad status" });
    var sh = sheet_(), v = sh.getDataRange().getValues();
    for (var i = 1; i < v.length; i++) {
      if (String(v[i][0]) === String(b.id)) {
        sh.getRange(i + 1, 4).setValue(b.status);
        sh.getRange(i + 1, 5).setValue(b.status === "done" ? new Date() : "");
        return json_({ ok: true, shoots: read_() });
      }
    }
    return json_({ ok: false, error: "unknown shoot" });
  } finally {
    lock.releaseLock();
  }
}
