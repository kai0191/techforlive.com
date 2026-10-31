(function () {
  // "5 min ago" labels
  function ago(iso) {
    var s = (Date.now() - new Date(iso).getTime()) / 1000;
    if (s < 60) return "just now";
    if (s < 3600) return Math.floor(s / 60) + " min ago";
    if (s < 86400) return Math.floor(s / 3600) + " h ago";
    return Math.floor(s / 86400) + " d ago";
  }
  function tick() {
    document.querySelectorAll("time[data-ago]").forEach(function (t) { t.textContent = ago(t.getAttribute("datetime")); });
  }
  tick(); setInterval(tick, 60000);

  // Tell readers when the wire has new stories since the page loaded
  var meta = document.querySelector('meta[name="tfl-updated"]');
  if (meta) {
    var loaded = meta.content;
    setInterval(function () {
      fetch("/data/latest.json?t=" + Date.now()).then(function (r) { return r.json(); }).then(function (d) {
        if (d.updated && d.updated > loaded) { var b = document.getElementById("newbar"); if (b) b.hidden = false; }
      }).catch(function () {});
    }, 300000);
  }

  // Live Hacker News front page, straight from the public Algolia API
  var hn = document.getElementById("hnlive");
  function loadHN() {
    fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=8").then(function (r) { return r.json(); }).then(function (d) {
      hn.innerHTML = "";
      d.hits.forEach(function (h) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = h.url || ("https://news.ycombinator.com/item?id=" + h.objectID);
        a.rel = "nofollow noopener"; a.target = "_blank"; a.textContent = h.title;
        var sm = document.createElement("small");
        sm.textContent = " · " + (h.points || 0) + " pts · " + ago(h.created_at);
        li.appendChild(a); li.appendChild(sm); hn.appendChild(li);
      });
    }).catch(function () { hn.innerHTML = '<li class="muted">Could not reach Hacker News right now.</li>'; });
  }
  if (hn) { loadHN(); setInterval(loadHN, 300000); }
})();
