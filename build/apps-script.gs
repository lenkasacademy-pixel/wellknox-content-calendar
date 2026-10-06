// Wellknox October 2026 status API, bound to the sheet "Wellknox Oct 2026 shoots".
// Tab "Shoots": A shoot_id, B place, C date, D status (planned or done), E updated_at.
// Tab "Posts":  A post_key, B status (pending, approved, changes, uploaded), C updated_at.
var SHEET_ID = "1uQhY5uvvJCKTgKXeu-HerCdRKexEs6vFkZwyrBIz524";
var TZ = "Asia/Kolkata";
var SEED = [
  ["shoot_id", "place", "date", "status", "updated_at"],
  ["s-hitech", "Hi-Tech City", "2026-10-09", "planned", ""],
  ["s-kukatpally", "Kukatpally", "2026-10-12", "planned", ""]
];

function shootSheet_() {
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
  if (sh.getLastRow() < 1) {
    sh.setName("Shoots");
    sh.getRange(1, 1, SEED.length, 5).setValues(SEED);
    sh.getRange(1, 1, 1, 5).setFontWeight("bold");
    sh.setFrozenRows(1);
    sh.autoResizeColumns(1, 5);
  }
  return sh;
}

function postSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID), sh = ss.getSheetByName("Posts");
  if (!sh) {
    sh = ss.insertSheet("Posts");
    sh.getRange(1, 1, 1, 3).setValues([["post_key", "status", "updated_at"]]);
    sh.getRange(1, 1, 1, 3).setFontWeight("bold");
    sh.setFrozenRows(1);
  }
  return sh;
}

function setup() { shootSheet_(); postSheet_(); }

function iso_(x) { return x instanceof Date ? x.toISOString() : (x ? String(x) : ""); }

function readShoots_() {
  var v = shootSheet_().getDataRange().getValues(), out = [];
  for (var i = 1; i < v.length; i++) {
    if (!v[i][0]) continue;
    var d = v[i][2];
    out.push({
      id: String(v[i][0]),
      place: String(v[i][1]),
      date: d instanceof Date ? Utilities.formatDate(d, TZ, "yyyy-MM-dd") : String(d),
      status: String(v[i][3] || "planned"),
      at: iso_(v[i][4])
    });
  }
  return out;
}

function readPosts_() {
  var v = postSheet_().getDataRange().getValues(), out = [];
  for (var i = 1; i < v.length; i++) {
    if (!v[i][0]) continue;
    out.push({ id: String(v[i][0]), status: String(v[i][1] || "pending"), at: iso_(v[i][2]) });
  }
  return out;
}

function all_() { return { ok: true, shoots: readShoots_(), posts: readPosts_() }; }

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() { return json_(all_()); }

function fail_(m) { return json_({ ok: false, error: m }); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var b = JSON.parse(e.postData.contents), type = b.type || "shoot";

    if (type === "shoot") {
      if (b.status !== "done" && b.status !== "planned") return fail_("bad status");
      var sh = shootSheet_(), v = sh.getDataRange().getValues();
      for (var i = 1; i < v.length; i++) {
        if (String(v[i][0]) === String(b.id)) {
          sh.getRange(i + 1, 4).setValue(b.status);
          sh.getRange(i + 1, 5).setValue(b.status === "done" ? new Date() : "");
          return json_(all_());
        }
      }
      return fail_("unknown shoot");
    }

    if (type === "addShoot") {
      var place = String(b.place || "").replace(/\s+/g, " ").trim();
      if (!place || place.length > 40) return fail_("bad place");
      if (!/^2026-10-(0[1-9]|[12][0-9]|3[01])$/.test(String(b.date))) return fail_("bad date");
      var s2 = shootSheet_();
      if (s2.getLastRow() > 40) return fail_("too many shoots");
      var row = s2.getLastRow() + 1;
      s2.getRange(row, 3).setNumberFormat("@");
      s2.getRange(row, 1, 1, 5).setValues([["s-" + Date.now().toString(36), place, String(b.date), "planned", ""]]);
      return json_(all_());
    }

    if (type === "post") {
      var ok = { pending: 1, approved: 1, changes: 1, uploaded: 1 };
      if (!ok[b.status]) return fail_("bad status");
      if (!/^[a-z0-9-]{1,30}$/.test(String(b.id))) return fail_("bad post");
      var ps = postSheet_(), pv = ps.getDataRange().getValues();
      for (var j = 1; j < pv.length; j++) {
        if (String(pv[j][0]) === String(b.id)) {
          ps.getRange(j + 1, 2, 1, 2).setValues([[b.status, new Date()]]);
          return json_(all_());
        }
      }
      ps.appendRow([String(b.id), b.status, new Date()]);
      return json_(all_());
    }

    return fail_("unknown request");
  } finally {
    lock.releaseLock();
  }
}
