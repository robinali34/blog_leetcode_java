(function () {
  var config = window.__translateConfig || {};
  var widget = document.querySelector("[data-translate-widget]");
  if (!config.enabled || !widget) {
    return;
  }

  var scriptLoaded = false;
  var statusEl = widget.querySelector("[data-translate-status]");

  function showStatus(message) {
    if (!statusEl) {
      return;
    }
    statusEl.textContent = message;
    statusEl.hidden = false;
  }

  function cookieDomain() {
    var host = location.hostname;
    if (!host || host === "localhost" || /^\d+\.\d+\.\d+\.\d+$/.test(host)) {
      return "";
    }
    var parts = host.split(".");
    if (parts.length >= 2) {
      return "." + parts.slice(-2).join(".");
    }
    return host;
  }

  function setTranslateCookie(value) {
    var base = "googtrans=" + value + "; path=/";
    document.cookie = base;
    var domain = cookieDomain();
    if (domain) {
      document.cookie = base + "; domain=" + domain;
    }
  }

  function clearTranslateCookie() {
    var expired = "Thu, 01 Jan 1970 00:00:00 GMT";
    document.cookie = "googtrans=; expires=" + expired + "; path=/";
    var domain = cookieDomain();
    if (domain) {
      document.cookie = "googtrans=; expires=" + expired + "; path=/; domain=" + domain;
    }
  }

  function currentLanguage() {
    var match = document.cookie.match(/(?:^|;\s*)googtrans=([^;]+)/);
    if (!match) {
      return "en";
    }
    var parts = decodeURIComponent(match[1]).split("/");
    return parts.length > 2 ? parts[2] : "en";
  }

  function markActiveLanguage() {
    var active = currentLanguage();
    widget.querySelectorAll("[data-translate-lang]").forEach(function (button) {
      var lang = button.getAttribute("data-translate-lang");
      button.classList.toggle("is-active", lang === active);
      button.setAttribute("aria-pressed", lang === active ? "true" : "false");
    });

    if (active === "zh-CN") {
      showStatus("当前为简体中文（机器翻译）");
    } else if (active === "zh-TW") {
      showStatus("當前為繁體中文（機器翻譯）");
    } else if (statusEl) {
      statusEl.hidden = true;
    }
  }

  function loadGoogleTranslate() {
    if (scriptLoaded) {
      return Promise.resolve();
    }

    scriptLoaded = true;
    showStatus("正在加载翻译组件…");

    return new Promise(function (resolve, reject) {
      window.googleTranslateElementInit = function () {
        /* global google */
        new google.translate.TranslateElement(
          {
            pageLanguage: config.pageLanguage || "en",
            includedLanguages: config.includedLanguages || "zh-CN,zh-TW",
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false,
          },
          "google_translate_element"
        );
        resolve();
      };

      var script = document.createElement("script");
      script.src =
        "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      script.onerror = function () {
        showStatus("翻译组件加载失败，请稍后重试。");
        reject(new Error("translate script failed"));
      };
      document.head.appendChild(script);
    });
  }

  function applyLanguage(lang) {
    if (lang === "en") {
      clearTranslateCookie();
      location.reload();
      return;
    }

    var source = config.pageLanguage || "en";
    setTranslateCookie("/" + source + "/" + lang);
    location.reload();
  }

  widget.querySelectorAll("[data-translate-lang]").forEach(function (button) {
    button.addEventListener("click", function () {
      var lang = button.getAttribute("data-translate-lang");
      if (lang === "en") {
        applyLanguage("en");
        return;
      }

      loadGoogleTranslate()
        .then(function () {
          applyLanguage(lang);
        })
        .catch(function () {
          /* status already shown */
        });
    });
  });

  markActiveLanguage();
})();
