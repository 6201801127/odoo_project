! function(e, t) {
    if ("function" == typeof define && define.amd) define(["exports"], t);
    else if ("undefined" != typeof exports) t(exports);
    else {
        var n = {};
        t(n), e.jsYearCalendar = n
    }
}("undefined" != typeof globalThis ? globalThis : "undefined" != typeof self ? self : this, function(e) {
    "use strict";

    function t(e) { return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) { return typeof e } : function(e) { return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e })(e) }

    function a(e, t) {
        for (var n = 0; n < t.length; n++) {
            var a = t[n];
            a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(e, a.key, a)
        }
    }

    function i(e, t, n) { return t in e ? Object.defineProperty(e, t, { value: n, enumerable: !0, configurable: !0, writable: !0 }) : e[t] = n, e }
    if (Object.defineProperty(e, "__esModule", { value: !0 }), e.default = void 0, "undefined" == typeof NodeList || NodeList.prototype.forEach || (NodeList.prototype.forEach = function(e, t) { t = t || window; for (var n = 0; n < this.length; n++) e.call(t, this[n], n, this) }), "undefined" != typeof Element && !Element.prototype.matches) {
        var n = Element.prototype;
        Element.prototype.matches = n.msMatchesSelector || n.webkitMatchesSelector
    }
    "undefined" == typeof Element || Element.prototype.closest || (Element.prototype.closest = function(e) {
        var t = this;
        if (!document.documentElement.contains(t)) return null;
        do {
            if (t.matches(e)) return t;
            t = t.parentElement || t.parentNode
        } while (null !== t && 1 == t.nodeType);
        return null
    });
    var s = function() {
        function D(e) {
            var t = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : null;
            if (function(e, t) { if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function") }(this, D), i(this, "element", void 0), i(this, "options", void 0), i(this, "_dataSource", void 0), i(this, "_mouseDown", void 0), i(this, "_rangeStart", void 0), i(this, "_rangeEnd", void 0), i(this, "_responsiveInterval", void 0), i(this, "_nbCols", void 0), i(this, "clickDay", void 0), i(this, "dayContextMenu", void 0), i(this, "mouseOnDay", void 0), i(this, "mouseOutDay", void 0), i(this, "renderEnd", void 0), i(this, "selectRange", void 0), i(this, "yearChanged", void 0), e instanceof HTMLElement) this.element = e;
            else {
                if ("string" != typeof e) throw new Error("The element parameter should be a DOM node or a selector");
                this.element = document.querySelector(e)
            }
            this.element.classList.add("calendar"), this._initializeEvents(t), this._initializeOptions(t), this.setYear(this.options.startYear)
        }
        var e, t, n;
        return e = D, (t = [{ key: "_initializeOptions", value: function(e) { null == e && (e = {}), this.options = { startYear: isNaN(parseInt(e.startYear)) ? (new Date).getFullYear() : parseInt(e.startYear), minDate: e.minDate instanceof Date ? e.minDate : null, maxDate: e.maxDate instanceof Date ? e.maxDate : null, language: null != e.language && null != D.locales[e.language] ? e.language : "en", allowOverlap: null == e.allowOverlap || e.allowOverlap, displayWeekNumber: null != e.displayWeekNumber && e.displayWeekNumber, displayDisabledDataSource: null != e.displayDisabledDataSource && e.displayDisabledDataSource, displayHeader: null == e.displayHeader || e.displayHeader, alwaysHalfDay: null != e.alwaysHalfDay && e.alwaysHalfDay, enableRangeSelection: null != e.enableRangeSelection && e.enableRangeSelection, disabledDays: e.disabledDays instanceof Array ? e.disabledDays : [], disabledWeekDays: e.disabledWeekDays instanceof Array ? e.disabledWeekDays : [], hiddenWeekDays: e.hiddenWeekDays instanceof Array ? e.hiddenWeekDays : [], roundRangeLimits: null != e.roundRangeLimits && e.roundRangeLimits, dataSource: e.dataSource instanceof Array || "function" == typeof e.dataSource ? e.dataSource : [], style: "background" == e.style || "border" == e.style || "custom" == e.style ? e.style : "border", enableContextMenu: null != e.enableContextMenu && e.enableContextMenu, contextMenuItems: e.contextMenuItems instanceof Array ? e.contextMenuItems : [], customDayRenderer: "function" == typeof e.customDayRenderer ? e.customDayRenderer : null, customDataSourceRenderer: "function" == typeof e.customDataSourceRenderer ? e.customDataSourceRenderer : null, weekStart: isNaN(parseInt(e.weekStart)) ? null : parseInt(e.weekStart), loadingTemplate: "string" == typeof e.loadingTemplate || e.loadingTemplate instanceof HTMLElement ? e.loadingTemplate : null }, this.options.dataSource instanceof Array && (this._dataSource = this.options.dataSource, this._initializeDatasourceColors()) } }, { key: "_initializeEvents", value: function(e) { null == e && (e = []), e.yearChanged && this.element.addEventListener("yearChanged", e.yearChanged), e.renderEnd && this.element.addEventListener("renderEnd", e.renderEnd), e.clickDay && this.element.addEventListener("clickDay", e.clickDay), e.dayContextMenu && this.element.addEventListener("dayContextMenu", e.dayContextMenu), e.selectRange && this.element.addEventListener("selectRange", e.selectRange), e.mouseOnDay && this.element.addEventListener("mouseOnDay", e.mouseOnDay), e.mouseOutDay && this.element.addEventListener("mouseOutDay", e.mouseOutDay) } }, {
            key: "_fetchDataSource",
            value: function(e) {
                if ("function" == typeof this.options.dataSource) {
                    var t = this.options.dataSource;
                    if (2 == t.length) t(this.options.startYear, e);
                    else {
                        var n = t(this.options.startYear);
                        n instanceof Array ? e(n) : n.then(e)
                    }
                } else e(this.options.dataSource)
            }
        }, { key: "_initializeDatasourceColors", value: function() { for (var e = 0; e < this._dataSource.length; e++) null == this._dataSource[e].color && (this._dataSource[e].color = D.colors[e % D.colors.length]) } }, {
            key: "render",
            value: function() {
                for (var e = 0 < arguments.length && void 0 !== arguments[0] && arguments[0]; this.element.firstChild;) this.element.removeChild(this.element.firstChild);
                if (this.options.displayHeader && this._renderHeader(), e) this._renderLoading();
                else {
                    this._renderBody(), this._renderDataSource(), this._applyEvents();
                    var t = this.element.querySelector(".months-container");
                    t.style.opacity = "0", t.style.display = "block", t.style.transition = "opacity 0.5s", setTimeout(function() { t.style.opacity = "1", setTimeout(function() { return t.style.transition = "" }, 500) }, 0), this._triggerEvent("renderEnd", { currentYear: this.options.startYear })
                }
            }
        }, {
            key: "_renderHeader",
            value: function() {
                var e = document.createElement("div");
                e.classList.add("calendar-header");
                var t = document.createElement("table"),
                    n = document.createElement("th");
                n.classList.add("prev"), null != this.options.minDate && this.options.minDate > new Date(this.options.startYear - 1, 11, 31) && n.classList.add("disabled");
                var a = document.createElement("span");
                a.innerHTML = "&lsaquo;", n.appendChild(a), t.appendChild(n);
                var i = document.createElement("th");
                i.classList.add("year-title"), i.classList.add("year-neighbor2"), i.textContent = (this.options.startYear - 2).toString(), null != this.options.minDate && this.options.minDate > new Date(this.options.startYear - 2, 11, 31) && i.classList.add("disabled"), t.appendChild(i);
                var s = document.createElement("th");
                s.classList.add("year-title"), s.classList.add("year-neighbor"), s.textContent = (this.options.startYear - 1).toString(), null != this.options.minDate && this.options.minDate > new Date(this.options.startYear - 1, 11, 31) && s.classList.add("disabled"), t.appendChild(s);
                var o = document.createElement("th");
                o.classList.add("year-title"), o.textContent = this.options.startYear.toString(), t.appendChild(o);
                var r = document.createElement("th");
                r.classList.add("year-title"), r.classList.add("year-neighbor"), r.textContent = (this.options.startYear + 1).toString(), null != this.options.maxDate && this.options.maxDate < new Date(this.options.startYear + 1, 0, 1) && r.classList.add("disabled"), t.appendChild(r);
                var l = document.createElement("th");
                l.classList.add("year-title"), l.classList.add("year-neighbor2"), l.textContent = (this.options.startYear + 2).toString(), null != this.options.maxDate && this.options.maxDate < new Date(this.options.startYear + 2, 0, 1) && l.classList.add("disabled"), t.appendChild(l);
                var d = document.createElement("th");
                d.classList.add("next"), null != this.options.maxDate && this.options.maxDate < new Date(this.options.startYear + 1, 0, 1) && d.classList.add("disabled");
                var u = document.createElement("span");
                u.innerHTML = "&rsaquo;", d.appendChild(u), t.appendChild(d), e.appendChild(t), this.element.appendChild(e)
            }
        }, {
            key: "_renderBody",
            value: function() {
                var e = document.createElement("div");
                e.classList.add("months-container");
                for (var t = 0; t < 12; t++) {
                    var n = document.createElement("div");
                    n.classList.add("month-container"), n.dataset.monthId = t.toString(), this._nbCols && n.classList.add("month-".concat(this._nbCols));
                    var a = new Date(this.options.startYear, t, 1),
                        i = document.createElement("table");
                    i.classList.add("month");
                    var s = document.createElement("thead"),
                        o = document.createElement("tr"),
                        r = document.createElement("th");
                    r.classList.add("month-title"), r.setAttribute("colspan", this.options.displayWeekNumber ? "8" : "7"), r.textContent = D.locales[this.options.language].months[t], o.appendChild(r), s.appendChild(o);
                    var l = document.createElement("tr");
                    if (this.options.displayWeekNumber)(m = document.createElement("th")).classList.add("week-number"), m.textContent = D.locales[this.options.language].weekShort, l.appendChild(m);
                    var d = this.options.weekStart ? this.options.weekStart : D.locales[this.options.language].weekStart,
                        u = d;
                    do {
                        var c = document.createElement("th");
                        c.classList.add("day-header"), c.textContent = D.locales[this.options.language].daysMin[u], this._isHidden(u) && c.classList.add("hidden"), l.appendChild(c), 7 <= ++u && (u = 0)
                    } while (u != d);
                    s.appendChild(l), i.appendChild(s);
                    for (var h = new Date(a.getTime()), p = new Date(this.options.startYear, t + 1, 0); h.getDay() != d;) h.setDate(h.getDate() - 1);
                    for (; h <= p;) {
                        var y = document.createElement("tr");
                        if (this.options.displayWeekNumber) {
                            var m = document.createElement("td"),
                                f = new Date(h.getTime());
                            f.setDate(f.getDate() - d + 4), m.classList.add("week-number"), m.textContent = this.getWeekNumber(f).toString(), y.appendChild(m)
                        }
                        do {
                            var g = document.createElement("td");
                            if (g.classList.add("day"), this._isHidden(h.getDay()) && g.classList.add("hidden"), h < a) g.classList.add("old");
                            else if (p < h) g.classList.add("new");
                            else {
                                this._isDisabled(h) && g.classList.add("disabled");
                                var v = document.createElement("div");
                                v.classList.add("day-content"), v.textContent = h.getDate().toString(), g.appendChild(v), this.options.customDayRenderer && this.options.customDayRenderer(v, h)
                            }
                            y.appendChild(g), h.setDate(h.getDate() + 1)
                        } while (h.getDay() != d);
                        i.appendChild(y)
                    }
                    n.appendChild(i), e.appendChild(n)
                }
                this.element.appendChild(e)
            }
        }, {
            key: "_renderLoading",
            value: function() {
                var e = document.createElement("div");
                e.classList.add("calendar-loading-container"), e.style.minHeight = 200 * this._nbCols + "px";
                var t = document.createElement("div");
                if (t.classList.add("calendar-loading"), this.options.loadingTemplate) "string" == typeof this.options.loadingTemplate ? t.innerHTML = this.options.loadingTemplate : this.options.loadingTemplate instanceof HTMLElement && t.appendChild(this.options.loadingTemplate);
                else {
                    var n = document.createElement("div");
                    n.classList.add("calendar-spinner");
                    for (var a = 1; a <= 3; a++) {
                        var i = document.createElement("div");
                        i.classList.add("bounce".concat(a)), n.appendChild(i)
                    }
                    t.appendChild(n)
                }
                e.appendChild(t), this.element.appendChild(e)
            }
        }, {
            key: "_renderDataSource",
            value: function() {
                var r = this;
                null != this._dataSource && 0 < this._dataSource.length && this.element.querySelectorAll(".month-container").forEach(function(e) {
                    var s = parseInt(e.dataset.monthId),
                        t = new Date(r.options.startYear, s, 1),
                        n = new Date(r.options.startYear, s + 1, 1);
                    if ((null == r.options.minDate || n > r.options.minDate) && (null == r.options.maxDate || t <= r.options.maxDate)) {
                        for (var o = [], a = 0; a < r._dataSource.length; a++) r._dataSource[a].startDate >= n && !(r._dataSource[a].endDate < t) || o.push(r._dataSource[a]);
                        0 < o.length && e.querySelectorAll(".day-content").forEach(function(e) {
                            var t = new Date(r.options.startYear, s, parseInt(e.textContent)),
                                n = new Date(r.options.startYear, s, t.getDate() + 1),
                                a = [];
                            if ((null == r.options.minDate || t >= r.options.minDate) && (null == r.options.maxDate || t <= r.options.maxDate)) {
                                for (var i = 0; i < o.length; i++) o[i].startDate < n && o[i].endDate >= t && a.push(o[i]);
                                0 < a.length && (r.options.displayDisabledDataSource || !r._isDisabled(t)) && r._renderDataSourceDay(e, t, a)
                            }
                        })
                    }
                })
            }
        }, {
            key: "_renderDataSourceDay",
            value: function(e, t, n) {
                var a = e.parentElement;
                switch (this.options.style) {
                    case "border":
                        var i = 0;
                        if (1 == n.length ? i = 4 : n.length <= 3 ? i = 2 : a.style.boxShadow = "inset 0 -4px 0 0 black", 0 < i) {
                            for (var s = "", o = 0; o < n.length; o++) "" != s && (s += ","), s += "inset 0 -".concat((o + 1) * i, "px 0 0 ").concat(n[o].color);
                            a.style.boxShadow = s
                        }
                        break;
                    case "background":
                        a.style.backgroundColor = n[n.length - 1].color;
                        var r = t.getTime();
                        if (n[n.length - 1].startDate.getTime() == r)
                            if (a.classList.add("day-start"), n[n.length - 1].startHalfDay || this.options.alwaysHalfDay) {
                                a.classList.add("day-half");
                                var l = "transparent";
                                for (o = n.length - 2; 0 <= o; o--)
                                    if (n[o].startDate.getTime() != r || !n[o].startHalfDay && !this.options.alwaysHalfDay) { l = n[o].color; break }
                                a.style.background = "linear-gradient(-45deg, ".concat(n[n.length - 1].color, ", ").concat(n[n.length - 1].color, " 49%, ").concat(l, " 51%, ").concat(l, ")")
                            } else this.options.roundRangeLimits && a.classList.add("round-left");
                        else if (n[n.length - 1].endDate.getTime() == r)
                            if (a.classList.add("day-end"), n[n.length - 1].endHalfDay || this.options.alwaysHalfDay) {
                                a.classList.add("day-half");
                                for (l = "transparent", o = n.length - 2; 0 <= o; o--)
                                    if (n[o].endDate.getTime() != r || !n[o].endHalfDay && !this.options.alwaysHalfDay) { l = n[o].color; break }
                                a.style.background = "linear-gradient(135deg, ".concat(n[n.length - 1].color, ", ").concat(n[n.length - 1].color, " 49%, ").concat(l, " 51%, ").concat(l, ")")
                            } else this.options.roundRangeLimits && a.classList.add("round-right");
                        break;
                    case "custom":
                        this.options.customDataSourceRenderer && this.options.customDataSourceRenderer.call(this, e, t, n)
                }
            }
        }, {
            key: "_applyEvents",
            value: function() {
                var s = this;
                this.options.displayHeader && (this.element.querySelectorAll(".year-neighbor, .year-neighbor2").forEach(function(e) { e.addEventListener("click", function(e) { e.currentTarget.classList.contains("disabled") || s.setYear(parseInt(e.currentTarget.textContent)) }) }), this.element.querySelector(".calendar-header .prev").addEventListener("click", function(e) {
                    if (!e.currentTarget.classList.contains("disabled")) {
                        var t = s.element.querySelector(".months-container");
                        t.style.transition = "margin-left 0.1s", t.style.marginLeft = "100%", setTimeout(function() { t.style.visibility = "hidden", t.style.transition = "", t.style.marginLeft = "0", setTimeout(function() { s.setYear(s.options.startYear - 1) }, 50) }, 100)
                    }
                }), this.element.querySelector(".calendar-header .next").addEventListener("click", function(e) {
                    if (!e.currentTarget.classList.contains("disabled")) {
                        var t = s.element.querySelector(".months-container");
                        t.style.transition = "margin-left 0.1s", t.style.marginLeft = "-100%", setTimeout(function() { t.style.visibility = "hidden", t.style.transition = "", t.style.marginLeft = "0", setTimeout(function() { s.setYear(s.options.startYear + 1) }, 50) }, 100)
                    }
                })), this.element.querySelectorAll(".day:not(.old):not(.new):not(.disabled)").forEach(function(e) {
                    e.addEventListener("click", function(e) {
                        e.stopPropagation();
                        var t = s._getDate(e.currentTarget);
                        s._triggerEvent("clickDay", { element: e.currentTarget, date: t, events: s.getEvents(t) })
                    }), e.addEventListener("contextmenu", function(e) {
                        s.options.enableContextMenu && (e.preventDefault(), 0 < s.options.contextMenuItems.length && s._openContextMenu(e.currentTarget));
                        var t = s._getDate(e.currentTarget);
                        s._triggerEvent("dayContextMenu", { element: e.currentTarget, date: t, events: s.getEvents(t) })
                    }), s.options.enableRangeSelection && (e.addEventListener("mousedown", function(e) {
                        if (1 == e.which) {
                            var t = s._getDate(e.currentTarget);
                            (s.options.allowOverlap || s.isThereFreeSlot(t)) && (s._mouseDown = !0, s._rangeStart = s._rangeEnd = t, s._refreshRange())
                        }
                    }), e.addEventListener("mouseenter", function(e) {
                        if (s._mouseDown) {
                            var t = s._getDate(e.currentTarget);
                            if (!s.options.allowOverlap) {
                                var n = new Date(s._rangeStart.getTime());
                                if (n < t)
                                    for (var a = new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1); n < t && s.isThereFreeSlot(a, !1);) n.setDate(n.getDate() + 1), a.setDate(a.getDate() + 1);
                                else
                                    for (a = new Date(n.getFullYear(), n.getMonth(), n.getDate() - 1); t < n && s.isThereFreeSlot(a, !0);) n.setDate(n.getDate() - 1), a.setDate(a.getDate() - 1);
                                t = n
                            }
                            var i = s._rangeEnd;
                            s._rangeEnd = t, i.getTime() != s._rangeEnd.getTime() && s._refreshRange()
                        }
                    })), e.addEventListener("mouseenter", function(e) {
                        if (!s._mouseDown) {
                            var t = s._getDate(e.currentTarget);
                            s._triggerEvent("mouseOnDay", { element: e.currentTarget, date: t, events: s.getEvents(t) })
                        }
                    }), e.addEventListener("mouseleave", function(e) {
                        var t = s._getDate(e.currentTarget);
                        s._triggerEvent("mouseOutDay", { element: e.currentTarget, date: t, events: s.getEvents(t) })
                    })
                }), this.options.enableRangeSelection && window.addEventListener("mouseup", function(e) {
                    if (s._mouseDown) {
                        s._mouseDown = !1, s._refreshRange();
                        var t = s._rangeStart < s._rangeEnd ? s._rangeStart : s._rangeEnd,
                            n = s._rangeEnd > s._rangeStart ? s._rangeEnd : s._rangeStart;
                        s._triggerEvent("selectRange", { startDate: t, endDate: n, events: s.getEventsOnRange(t, new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1)) })
                    }
                }), this._responsiveInterval && (clearInterval(this._responsiveInterval), this._responsiveInterval = null), this._responsiveInterval = setInterval(function() {
                    if (null != s.element.querySelector(".month")) {
                        var e = s.element.offsetWidth,
                            t = s.element.querySelector(".month").offsetWidth + 10;
                        s._nbCols = null, s._nbCols = 6 * t < e ? 2 : 4 * t < e ? 3 : 3 * t < e ? 4 : 2 * t < e ? 6 : 12, s.element.querySelectorAll(".month-container").forEach(function(t) { t.classList.contains("month-".concat(s._nbCols)) || (["month-2", "month-3", "month-4", "month-6", "month-12"].forEach(function(e) { t.classList.remove(e) }), t.classList.add("month-".concat(s._nbCols))) })
                    }
                }, 300)
            }
        }, {
            key: "_refreshRange",
            value: function() {
                var n = this;
                if (this.element.querySelectorAll("td.day.range").forEach(function(e) { return e.classList.remove("range") }), this.element.querySelectorAll("td.day.range-start").forEach(function(e) { return e.classList.remove("range-start") }), this.element.querySelectorAll("td.day.range-end").forEach(function(e) { return e.classList.remove("range-end") }), this._mouseDown) {
                    var a = this._rangeStart < this._rangeEnd ? this._rangeStart : this._rangeEnd,
                        i = this._rangeEnd > this._rangeStart ? this._rangeEnd : this._rangeStart;
                    this.element.querySelectorAll(".month-container").forEach(function(e) {
                        var t = parseInt(e.dataset.monthId);
                        a.getMonth() <= t && i.getMonth() >= t && e.querySelectorAll("td.day:not(.old):not(.new)").forEach(function(e) {
                            var t = n._getDate(e);
                            a <= t && t <= i && (e.classList.add("range"), t.getTime() == a.getTime() && e.classList.add("range-start"), t.getTime() == i.getTime() && e.classList.add("range-end"))
                        })
                    })
                }
            }
        }, { key: "_getElementPosition", value: function(e) { for (var t = 0, n = 0; t += e.offsetTop || 0, n += e.offsetLeft || 0, e = e.offsetParent;); return { top: t, left: n } } }, {
            key: "_openContextMenu",
            value: function(e) {
                var t = this,
                    n = document.querySelector(".calendar-context-menu");
                if (null !== n)
                    for (n.style.display = "none"; n.firstChild;) n.removeChild(n.firstChild);
                else(n = document.createElement("div")).classList.add("calendar-context-menu"), document.body.appendChild(n);
                for (var a = this._getDate(e), i = this.getEvents(a), s = 0; s < i.length; s++) {
                    var o = document.createElement("div");
                    o.classList.add("item"), o.style.paddingLeft = "4px", o.style.boxShadow = "inset 4px 0 0 0 ".concat(i[s].color);
                    var r = document.createElement("div");
                    r.classList.add("content");
                    var l = document.createElement("span");
                    l.classList.add("text"), l.textContent = i[s].name, r.appendChild(l);
                    var d = document.createElement("span");
                    d.classList.add("arrow"), d.innerHTML = "&rsaquo;", r.appendChild(d), o.appendChild(r), this._renderContextMenuItems(o, this.options.contextMenuItems, i[s]), n.appendChild(o)
                }
                if (0 < n.children.length) {
                    var u = this._getElementPosition(e);
                    n.style.left = u.left + 25 + "px", n.style.right = "", n.style.top = u.top + 25 + "px", n.style.display = "block", n.getBoundingClientRect().right > document.body.offsetWidth && (n.style.left = "", n.style.right = "0"), setTimeout(function() { return t._checkContextMenuItemsPosition() }, 0);
                    var c = function e(t) { "click" === t.type && n.contains(t.target) || (n.style.display = "none", window.removeEventListener("click", e), window.removeEventListener("resize", e), window.removeEventListener("scroll", e)) };
                    window.addEventListener("click", c), window.addEventListener("resize", c), window.addEventListener("scroll", c)
                }
            }
        }, {
            key: "_renderContextMenuItems",
            value: function(e, t, n) {
                var a = document.createElement("div");
                a.classList.add("submenu");
                for (var i = 0; i < t.length; i++)
                    if (!1 !== t[i].visible && ("function" != typeof t[i].visible || t[i].visible(n))) {
                        var s = document.createElement("div");
                        s.classList.add("item");
                        var o = document.createElement("div");
                        o.classList.add("content");
                        var r = document.createElement("span");
                        if (r.classList.add("text"), r.textContent = t[i].text, o.appendChild(r), t[i].click && function(e) { o.addEventListener("click", function() { document.querySelector(".calendar-context-menu").style.display = "none", t[e].click(n) }) }(i), s.appendChild(o), t[i].items && 0 < t[i].items.length) {
                            var l = document.createElement("span");
                            l.classList.add("arrow"), l.innerHTML = "&rsaquo;", o.appendChild(l), this._renderContextMenuItems(s, t[i].items, n)
                        }
                        a.appendChild(s)
                    }
                0 < a.children.length && e.appendChild(a)
            }
        }, {
            key: "_checkContextMenuItemsPosition",
            value: function() {
                var e = document.querySelectorAll(".calendar-context-menu .submenu");
                e.forEach(function(e) {
                    var t = e;
                    t.style.display = "block", t.style.visibility = "hidden"
                }), e.forEach(function(e) {
                    var t = e;
                    t.getBoundingClientRect().right > document.body.offsetWidth ? t.classList.add("open-left") : t.classList.remove("open-left")
                }), e.forEach(function(e) {
                    var t = e;
                    t.style.display = "", t.style.visibility = ""
                })
            }
        }, {
            key: "_getDate",
            value: function(e) {
                var t = e.querySelector(".day-content").textContent,
                    n = e.closest(".month-container").dataset.monthId,
                    a = this.options.startYear;
                return new Date(a, n, t)
            }
        }, { key: "_triggerEvent", value: function(e, t) { var n = null; for (var a in "function" == typeof Event ? n = new Event(e) : (n = document.createEvent("Event")).initEvent(e, !1, !1), n.calendar = this, t) n[a] = t[a]; return this.element.dispatchEvent(n), n } }, {
            key: "_isDisabled",
            value: function(e) {
                if (null != this.options.minDate && e < this.options.minDate || null != this.options.maxDate && e > this.options.maxDate) return !0;
                if (0 < this.options.disabledWeekDays.length)
                    for (var t = 0; t < this.options.disabledWeekDays.length; t++)
                        if (e.getDay() == this.options.disabledWeekDays[t]) return !0;
                if (0 < this.options.disabledDays.length)
                    for (t = 0; t < this.options.disabledDays.length; t++)
                        if (e.getTime() == this.options.disabledDays[t].getTime()) return !0;
                return !1
            }
        }, {
            key: "_isHidden",
            value: function(e) {
                if (0 < this.options.hiddenWeekDays.length)
                    for (var t = 0; t < this.options.hiddenWeekDays.length; t++)
                        if (e == this.options.hiddenWeekDays[t]) return !0;
                return !1
            }
        }, {
            key: "getWeekNumber",
            value: function(e) {
                var t = new Date(e.getTime());
                t.setHours(0, 0, 0, 0), t.setDate(t.getDate() + 3 - (t.getDay() + 6) % 7);
                var n = new Date(t.getFullYear(), 0, 4);
                return 1 + Math.round(((t.getTime() - n.getTime()) / 864e5 - 3 + (n.getDay() + 6) % 7) / 7)
            }
        }, { key: "getEvents", value: function(e) { return this.getEventsOnRange(e, new Date(e.getFullYear(), e.getMonth(), e.getDate() + 1)) } }, {
            key: "getEventsOnRange",
            value: function(e, t) {
                var n = [];
                if (this._dataSource && e && t)
                    for (var a = 0; a < this._dataSource.length; a++) this._dataSource[a].startDate < t && this._dataSource[a].endDate >= e && n.push(this._dataSource[a]);
                return n
            }
        }, {
            key: "isThereFreeSlot",
            value: function(t) {
                var n = this,
                    e = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : null,
                    a = this.getEvents(t);
                return !0 === e ? !a.some(function(e) { return !n.options.alwaysHalfDay && !e.endHalfDay || e.endDate > t }) : !1 === e ? !a.some(function(e) { return !n.options.alwaysHalfDay && !e.startHalfDay || e.startDate < t }) : this.isThereFreeSlot(t, !1) || this.isThereFreeSlot(t, !0)
            }
        }, { key: "getYear", value: function() { return this.options.startYear } }, {
            key: "setYear",
            value: function(e) {
                var t = this,
                    n = parseInt(e);
                if (!isNaN(n)) {
                    for (this.options.startYear = n; this.element.firstChild;) this.element.removeChild(this.element.firstChild);
                    this.options.displayHeader && this._renderHeader();
                    var a = this._triggerEvent("yearChanged", { currentYear: this.options.startYear, preventRendering: !1 });
                    "function" == typeof this.options.dataSource ? (this.render(!0), this._fetchDataSource(function(e) { t._dataSource = e, t._initializeDatasourceColors(), t.render(!1) })) : a.preventRendering || this.render()
                }
            }
        }, { key: "getMinDate", value: function() { return this.options.minDate } }, {
            key: "setMinDate",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                (e instanceof Date || null === e) && (this.options.minDate = e, t || this.render())
            }
        }, { key: "getMaxDate", value: function() { return this.options.maxDate } }, {
            key: "setMaxDate",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                (e instanceof Date || null === e) && (this.options.maxDate = e, t || this.render())
            }
        }, { key: "getStyle", value: function() { return this.options.style } }, {
            key: "setStyle",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.style = "background" == e || "border" == e || "custom" == e ? e : "border", t || this.render()
            }
        }, { key: "getAllowOverlap", value: function() { return this.options.allowOverlap } }, { key: "setAllowOverlap", value: function(e) { this.options.allowOverlap = e } }, { key: "getDisplayWeekNumber", value: function() { return this.options.displayWeekNumber } }, {
            key: "setDisplayWeekNumber",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.displayWeekNumber = e, t || this.render()
            }
        }, { key: "getDisplayHeader", value: function() { return this.options.displayHeader } }, {
            key: "setDisplayHeader",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.displayHeader = e, t || this.render()
            }
        }, { key: "getDisplayDisabledDataSource", value: function() { return this.options.displayDisabledDataSource } }, {
            key: "setDisplayDisabledDataSource",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.displayDisabledDataSource = e, t || this.render()
            }
        }, { key: "getAlwaysHalfDay", value: function() { return this.options.alwaysHalfDay } }, {
            key: "setAlwaysHalfDay",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.alwaysHalfDay = e, t || this.render()
            }
        }, { key: "getEnableRangeSelection", value: function() { return this.options.enableRangeSelection } }, {
            key: "setEnableRangeSelection",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.enableRangeSelection = e, t || this.render()
            }
        }, { key: "getDisabledDays", value: function() { return this.options.disabledDays } }, {
            key: "setDisabledDays",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.disabledDays = e instanceof Array ? e : [], t || this.render()
            }
        }, { key: "getDisabledWeekDays", value: function() { return this.options.disabledWeekDays } }, {
            key: "setDisabledWeekDays",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.disabledWeekDays = e instanceof Array ? e : [], t || this.render()
            }
        }, { key: "getHiddenWeekDays", value: function() { return this.options.hiddenWeekDays } }, {
            key: "setHiddenWeekDays",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.hiddenWeekDays = e instanceof Array ? e : [], t || this.render()
            }
        }, { key: "getRoundRangeLimits", value: function() { return this.options.roundRangeLimits } }, {
            key: "setRoundRangeLimits",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.roundRangeLimits = e, t || this.render()
            }
        }, { key: "getEnableContextMenu", value: function() { return this.options.enableContextMenu } }, {
            key: "setEnableContextMenu",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.enableContextMenu = e, t || this.render()
            }
        }, { key: "getContextMenuItems", value: function() { return this.options.contextMenuItems } }, {
            key: "setContextMenuItems",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.contextMenuItems = e instanceof Array ? e : [], t || this.render()
            }
        }, { key: "getCustomDayRenderer", value: function() { return this.options.customDayRenderer } }, {
            key: "setCustomDayRenderer",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.customDayRenderer = "function" == typeof e ? e : null, t || this.render()
            }
        }, { key: "getCustomDataSourceRenderer", value: function() { return this.options.customDataSourceRenderer } }, {
            key: "setCustomDataSourceRenderer",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.customDataSourceRenderer = "function" == typeof e ? e : null, t || this.render()
            }
        }, { key: "getLanguage", value: function() { return this.options.language } }, {
            key: "setLanguage",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                null != e && null != D.locales[e] && (this.options.language = e, t || this.render())
            }
        }, { key: "getDataSource", value: function() { return this.options.dataSource } }, {
            key: "setDataSource",
            value: function(e) {
                var t = this,
                    n = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.dataSource = e instanceof Array || "function" == typeof e ? e : [], "function" == typeof this.options.dataSource ? (this.render(!0), this._fetchDataSource(function(e) { t._dataSource = e, t._initializeDatasourceColors(), t.render(!1) })) : (this._dataSource = this.options.dataSource, this._initializeDatasourceColors(), n || this.render())
            }
        }, { key: "getWeekStart", value: function() { return this.options.weekStart ? this.options.weekStart : D.locales[this.options.language].weekStart } }, {
            key: "setWeekStart",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this.options.weekStart = isNaN(parseInt(e)) ? null : parseInt(e), t || this.render()
            }
        }, { key: "getLoadingTemplate", value: function() { return this.options.loadingTemplate } }, { key: "setLoadingTemplate", value: function(e) { this.options.loadingTemplate = "string" == typeof e || e instanceof HTMLElement ? e : null } }, {
            key: "addEvent",
            value: function(e) {
                var t = 1 < arguments.length && void 0 !== arguments[1] && arguments[1];
                this._dataSource.push(e), t || this.render()
            }
        }]) && a(e.prototype, t), n && a(e, n), D
    }();
    i(e.default = s, "locales", { en: { days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"], months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], weekShort: "W", weekStart: 0 } }), i(s, "colors", ["#2C8FC9", "#9CB703", "#F5BB00", "#FF4A32", "#B56CE2", "#45A597"]), "object" === ("undefined" == typeof window ? "undefined" : t(window)) && (window.Calendar = s, document.addEventListener("DOMContentLoaded", function() { document.querySelectorAll('[data-provide="calendar"]').forEach(function(e) { return new s(e) }) }))
});