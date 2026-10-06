// Wellknox shoot-status API.
// Paste this into Extensions > Apps Script of the Google Sheet "Wellknox Oct 2026 shoots",
// then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
// Copy the Web app URL into SHEETS_URL in build/build_calendar.py and rebuild.
// Columns: A shoot_id, B place, C date, D status (planned or done), E updated_at.

function sheet_() { return SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]; }

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
