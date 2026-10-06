(function () {
  var URL_ = __URL__;
  var KEY = "wk-live-v2", DOWN = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var LABEL = { pending: "Awaiting approval", approved: "Approved", changes: "Changes requested", uploaded: "Uploaded" };
  var st = { shoots: [], posts: {}, fromSheet: false };
  var live = document.getElementById("live"), list = document.querySelector(".sh-grid");
  var addBtn = document.getElementById("addshoot"), form = document.getElementById("addform"), msg = document.getElementById("ash-msg");
  try { var o = JSON.parse(localStorage.getItem(KEY) || "null"); if (o) { st.shoots = o.shoots || []; st.posts = o.posts || {}; } } catch (e) {}
  if (!st.shoots.length) {
    list.querySelectorAll(".shoot[data-sid]").forEach(function (c) {
      st.shoots.push({ id: c.getAttribute("data-sid"), place: c.querySelector("h4").textContent, date: c.getAttribute("data-date"), status: "planned", at: "" });
    });
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify({ shoots: st.shoots, posts: st.posts })); } catch (e) {} }
  function fmt(iso) { try { return new Date(iso).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }); } catch (e) { return ""; } }
  function setLive(t, ok) { live.textContent = t; live.className = "live" + (ok ? " on" : ""); }
  function dayNum(date) { var m = /^2026-10-(\d\d)$/.exec(date || ""); return m ? +m[1] : 0; }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  function ensureShoot(s) {
    var d = dayNum(s.date); if (!d) return;
    var card = list.querySelector('.shoot[data-sid="' + s.id + '"]');
    if (!card) {
      card = el("div", "shoot"); card.setAttribute("data-sid", s.id);
      var sd = el("div", "sd"); sd.appendChild(el("b")); sd.appendChild(el("span"));
      var sb = el("div", "sb"); sb.appendChild(el("h4")); var p = el("p", "ss", "Planned"); p.setAttribute("data-sstat", ""); sb.appendChild(p);
      var btn = el("button", "btn sbtn", "Mark shoot done"); btn.type = "button";
      card.appendChild(sd); card.appendChild(sb); card.appendChild(btn); list.appendChild(card);
    }
    card.setAttribute("data-date", s.date);
    card.querySelector(".sd b").textContent = d;
    card.querySelector(".sd span").textContent = DOWN[new Date(2026, 9, d).getDay()];
    card.querySelector("h4").textContent = s.place;
    var cell = document.querySelector('.cell[data-day="' + d + '"]');
    var chip = document.querySelector('.gshoot[data-sid="' + s.id + '"]');
    if (chip && (!cell || chip.parentNode !== cell)) { chip.remove(); chip = null; }
    if (!chip && cell) {
      chip = el("a", "gshoot"); chip.href = "#shoots"; chip.setAttribute("data-sid", s.id);
      chip.appendChild(el("i", "pip")); chip.appendChild(el("span", "gs-n")); chip.appendChild(el("span", "gs-t", "Planned")); cell.appendChild(chip);
    }
    if (chip) chip.querySelector(".gs-n").textContent = "Shoot · " + s.place;
  }
  function renderShoots() {
    var seen = {};
    st.shoots.forEach(function (s) {
      seen[s.id] = 1; ensureShoot(s);
      var done = s.status === "done";
      document.querySelectorAll('[data-sid="' + s.id + '"]').forEach(function (n) {
        n.classList.toggle("done", done);
        var t = n.querySelector("[data-sstat]"); if (t) t.textContent = done ? "Shoot done" + (s.at ? " · " + fmt(s.at) : "") : "Planned";
        var g = n.querySelector(".gs-t"); if (g) g.textContent = done ? "Done" : "Planned";
        var b = n.querySelector(".sbtn"); if (b) b.textContent = done ? "Undo" : "Mark shoot done";
      });
    });
    if (st.fromSheet) document.querySelectorAll("[data-sid]").forEach(function (n) { if (!seen[n.getAttribute("data-sid")]) n.remove(); });
    Array.prototype.slice.call(list.children).sort(function (a, b) {
      return (a.getAttribute("data-date") || "").localeCompare(b.getAttribute("data-date") || "");
    }).forEach(function (c) { list.appendChild(c); });
  }

  function statusOf(key) { return (st.posts[key] && st.posts[key].status) || "pending"; }
  function renderPosts() {
    document.querySelectorAll("[data-pkey]").forEach(function (n) {
      var s = statusOf(n.getAttribute("data-pkey")); n.setAttribute("data-status", s);
      var pill = n.querySelector("[data-pill]"); if (pill) { pill.textContent = LABEL[s]; pill.setAttribute("data-s", s); }
      var a = n.querySelector(".btn.ok .lb"); if (a) a.textContent = s === "approved" ? "Approved" : "Approve";
      var c = n.querySelector(".btn.ch .lb"); if (c) c.textContent = s === "changes" ? "Changes requested" : "Make changes";
      var u = n.querySelector(".btn.up .lb"); if (u) u.textContent = s === "uploaded" ? "Uploaded" : "Mark uploaded";
      var r = n.querySelector(".lnk"); if (r) r.hidden = s === "pending";
    });
  }

  function apply(j) {
    if (j.shoots) { st.shoots = j.shoots; st.fromSheet = true; }
    if (j.posts) { var m = {}; j.posts.forEach(function (r) { m[r.id] = { status: r.status, at: r.at }; }); st.posts = m; }
    save(); renderShoots(); renderPosts(); setLive("Live · updated " + fmt(new Date().toISOString()), true);
  }
  function post(body) {
    return fetch(URL_, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); });
  }
  function pull() {
    return fetch(URL_, { cache: "no-store" }).then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok) apply(j); })
      .catch(function () { setLive("Offline, showing the last saved status", false); });
  }
  function send(body) {
    post(body).then(function (j) { if (j && j.ok) apply(j); else setLive("The sheet did not accept that change", false); })
      .catch(function () { setLive("Could not reach the sheet. Try again.", false); });
  }
  function setPost(key, status) {
    st.posts[key] = { status: status, at: new Date().toISOString() }; save(); renderPosts();
    send({ type: "post", id: key, status: status });
  }

  if (!URL_) {
    document.querySelectorAll(".sbtn, .btn.up, .lnk, #addshoot").forEach(function (n) { n.remove(); });
    return;
  }

  list.addEventListener("click", function (e) {
    var b = e.target.closest(".sbtn"); if (!b) return;
    var id = b.closest("[data-sid]").getAttribute("data-sid");
    var s = st.shoots.filter(function (x) { return x.id === id; })[0]; if (!s) return;
    s.status = s.status === "done" ? "planned" : "done"; s.at = s.status === "done" ? new Date().toISOString() : "";
    save(); renderShoots(); send({ type: "shoot", id: id, status: s.status });
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-act]"); if (!b) return;
    var host = b.closest("[data-pkey]"); if (!host) return;
    var key = host.getAttribute("data-pkey"), act = b.getAttribute("data-act");
    if (act === "uploaded") act = statusOf(key) === "uploaded" ? "approved" : "uploaded";
    setPost(key, act);
  });

  addBtn.addEventListener("click", function () {
    form.hidden = !form.hidden; addBtn.setAttribute("aria-expanded", String(!form.hidden)); msg.textContent = "";
    if (!form.hidden) document.getElementById("ash-place").focus();
  });
  document.getElementById("ash-cancel").addEventListener("click", function () { form.hidden = true; addBtn.setAttribute("aria-expanded", "false"); });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var place = document.getElementById("ash-place").value.trim(), date = document.getElementById("ash-date").value;
    if (!place || !date) { msg.textContent = "Add a place and a date in October."; return; }
    msg.textContent = "Adding";
    post({ type: "addShoot", place: place, date: date }).then(function (j) {
      if (j && j.ok) { apply(j); form.reset(); form.hidden = true; addBtn.setAttribute("aria-expanded", "false"); msg.textContent = ""; }
      else msg.textContent = "Could not add that shoot. Check the place and date.";
    }).catch(function () { msg.textContent = "Could not reach the sheet. Try again."; });
  });

  renderShoots(); renderPosts(); setLive("Connecting to the sheet", false); pull();
  setInterval(function () { if (!document.hidden) pull(); }, 8000);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) pull(); });
})();
