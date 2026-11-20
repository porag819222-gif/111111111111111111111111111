#!/usr/bin/env python3
"""Taleora Studio static site generator.
Run:  python3 src/build.py   -> writes index.html (+ legacy route redirects) in the project root.
All customer CTAs point to the official Facebook page only.
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = "https://www.facebook.com/taleorastudio76"
REL = 'target="_blank" rel="noopener noreferrer"'

def t(e, b):
    return f'<span class="en">{e}</span><span class="bn">{b}</span>'

ICON = {
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 22v-8.2h2.8l.5-3.3h-3.3V8.4c0-.9.4-1.7 1.8-1.7h1.6V3.8c-.3 0-1.3-.2-2.4-.2-2.5 0-4.1 1.5-4.1 4.2v2.7H7.7v3.3h2.7V22z"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg>',
 "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
 # process icons (website journey)
 "choose": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><path d="m15 17.5 2 2 4-4.5"/></svg>',
 "details": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="m3.5 17 5-4.5 4 3.5 3-2.5 5 4M15 8h3"/></svg>',
 "build": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m8 8-4.5 4L8 16M16 8l4.5 4L16 16M13.5 5l-3 14"/></svg>',
 "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>',
 # why icons
 "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.5C19.5 15.4 12 20 12 20z"/></svg>',
 "film": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M17 9h4M3 15h4M17 15h4"/></svg>',
 "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
 "frame": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="17" height="17" rx="2"/><rect x="7" y="7" width="10" height="10" rx="1"/></svg>',
 "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16 9.5"/></svg>',
}

KIND = {"fixed": ("Fixed price", "নির্দিষ্ট মূল্য"),
        "from": ("Starting price", "শুরুর মূল্য"),
        "range": ("Price range", "মূল্যের পরিসর")}

# ---------------------------------------------------------------- DATA
# Prices / durations / delivery estimates are exactly as agreed. Inclusion lists come from the existing project.
VIDEO = [
 dict(id="stickman", en="Stickman Animation", bn="স্টিকম্যান অ্যানিমেশন", price="499", kind="fixed",
      dur=("30 seconds", "৩০ সেকেন্ড"), img="stickman", pos="50% 45%", cls="s5",
      desc=("A 30-second story told with custom stickman characters.", "কাস্টম স্টিকম্যান ক্যারেক্টারে ৩০ সেকেন্ডের গল্প।"),
      items=[("30 seconds", "৩০ সেকেন্ড"), ("Custom stickman characters", "কাস্টম স্টিকম্যান ক্যারেক্টার"), ("Simple storytelling", "সহজ গল্প বলা"), ("Basic animation & scene transitions", "বেসিক অ্যানিমেশন ও সিন ট্রানজিশন"), ("Concept based on your idea", "আপনার আইডিয়া অনুযায়ী কনসেপ্ট")],
      suit=("Simple, expressive stories and messages told through character.", "চরিত্রের মাধ্যমে সহজ, অভিব্যক্তিময় গল্প ও বার্তা বলার জন্য।")),
 dict(id="cinematic", en="AI Cinematic Video", bn="এআই সিনেমাটিক ভিডিও", price="1,499–৳1,999", kind="range",
      dur=("30 seconds", "৩০ সেকেন্ড"), img="ai-cinematic", pos="40% 50%", cls="s7 h",
      desc=("Cinematic visuals with emotional storytelling and sound.", "সিনেমাটিক ভিজ্যুয়াল, আবেগময় গল্প ও সাউন্ড ডিজাইন।"),
      items=[("30 seconds", "৩০ সেকেন্ড"), ("Cinematic AI-generated visuals", "সিনেমাটিক এআই ভিজ্যুয়াল"), ("Creative scene composition", "ক্রিয়েটিভ সিন কম্পোজিশন"), ("Professional editing", "প্রফেশনাল এডিটিং"), ("Background music & sound design", "ব্যাকগ্রাউন্ড মিউজিক ও সাউন্ড ডিজাইন"), ("Final price depends on complexity", "চূড়ান্ত মূল্য প্রজেক্টের জটিলতার ওপর নির্ভর করে")],
      suit=("Anyone who wants a film-like moment for a tribute, message or story idea.", "যারা কোনো শ্রদ্ধাঞ্জলি, বার্তা বা গল্পের আইডিয়াকে সিনেমার মতো রূপ দিতে চান।")),
 dict(id="story", en="Custom Animated Story", bn="কাস্টম অ্যানিমেটেড স্টোরি", price="2,499+", kind="from",
      dur=("1 minute", "১ মিনিট"), img="animated-story", pos="60% 40%", cls="s7 h",
      desc=("A one-minute story built around your characters and scenes.", "আপনার চরিত্র ও দৃশ্য নিয়ে ১ মিনিটের গল্প।"),
      items=[("1 minute", "১ মিনিট"), ("Personalized story concept", "পার্সোনালাইজড স্টোরি কনসেপ্ট"), ("Custom characters & scenes", "কাস্টম ক্যারেক্টার ও সিন"), ("Cinematic editing & transitions", "সিনেমাটিক এডিটিং ও ট্রানজিশন"), ("Music & sound design", "মিউজিক ও সাউন্ড ডিজাইন"), ("Quotation depends on complexity, characters, quality & duration", "কোটেশন নির্ভর করে জটিলতা, চরিত্র, কোয়ালিটি ও সময়ের ওপর")],
      suit=("Personal stories that need their own characters and scenes.", "যে ব্যক্তিগত গল্পের জন্য নিজস্ব চরিত্র ও দৃশ্য দরকার।")),
 dict(id="bday-video", en="Personalized Birthday Video", bn="পার্সোনালাইজড বার্থডে ভিডিও", price="699", kind="from",
      dur=("30–60 seconds", "৩০–৬০ সেকেন্ড"), img="birthday", pos="12% 60%", cls="s5",
      desc=("A heartfelt birthday video with the name and photos you choose.", "আপনার পছন্দের নাম ও ছবি দিয়ে সাজানো জন্মদিনের ভিডিও।"),
      items=[("30–60 seconds", "৩০–৬০ সেকেন্ড"), ("Personalized birthday message", "পার্সোনালাইজড বার্থডে মেসেজ"), ("Name & photo integration", "নাম ও ছবির সংযোজন"), ("Birthday-themed visuals", "বার্থডে থিমের ভিজ্যুয়াল"), ("Music & transitions", "মিউজিক ও ট্রানজিশন"), ("Special surprise presentation", "বিশেষ সারপ্রাইজ উপস্থাপনা")],
      suit=("Birthday surprises for friends, partners and family.", "বন্ধু, জীবনসঙ্গী ও পরিবারের জন্য জন্মদিনের সারপ্রাইজ।")),
]
WEB = [
 dict(id="web-simple", en="Simple Birthday Website", bn="সিম্পল বার্থডে ওয়েবসাইট", price="499", kind="fixed",
      deliv=("1–2 days", "১–২ দিন"), img="websites", pos="14% 55%", cls="s4",
      desc=("A clean personalized birthday page you can share with a link.", "লিংকে শেয়ার করার মতো সুন্দর বার্থডে পেজ।"),
      items=[("Personalized birthday homepage", "পার্সোনালাইজড বার্থডে হোমপেজ"), ("Recipient's name", "প্রাপকের নাম"), ("Birthday wishes & messages", "শুভেচ্ছা ও বার্তা"), ("Attractive birthday design", "আকর্ষণীয় বার্থডে ডিজাইন"), ("Mobile-friendly layout", "মোবাইল-ফ্রেন্ডলি লেআউট"), ("Shareable website link", "শেয়ারযোগ্য ওয়েবসাইট লিংক")],
      suit=("A quick, sweet birthday gift you can send with a link.", "একটি লিংকে পাঠিয়ে দেওয়ার মতো সহজ, মিষ্টি জন্মদিনের উপহার।")),
 dict(id="web-premium", en="Premium Birthday Website", bn="প্রিমিয়াম বার্থডে ওয়েবসাইট", price="899", kind="fixed",
      deliv=("2–3 days", "২–৩ দিন"), img="birthday", pos="50% 55%", cls="s4",
      desc=("An animated, interactive birthday experience with a memory gallery.", "অ্যানিমেটেড ও ইন্টারঅ্যাক্টিভ বার্থডে এক্সপেরিয়েন্স।"),
      items=[("Premium personalized design", "প্রিমিয়াম পার্সোনালাইজড ডিজাইন"), ("Animated sections", "অ্যানিমেটেড সেকশন"), ("Wishes & special messages", "শুভেচ্ছা ও বিশেষ বার্তা"), ("Photo & memory gallery", "ছবি ও স্মৃতির গ্যালারি"), ("Interactive surprise elements", "ইন্টারঅ্যাক্টিভ সারপ্রাইজ"), ("Smooth transitions", "স্মুথ ট্রানজিশন"), ("Mobile-responsive", "মোবাইল-রেসপন্সিভ")],
      suit=("Surprises that deserve animation and a gallery of memories.", "অ্যানিমেশন ও স্মৃতির গ্যালারির যোগ্য সারপ্রাইজের জন্য।")),
 dict(id="web-love", en="Love Story Website", bn="লাভ স্টোরি ওয়েবসাইট", price="1,199", kind="fixed",
      deliv=("2–3 days", "২–৩ দিন"), img="love-story", pos="50% 55%", cls="s4",
      desc=("Your story as a cinematic scrolling journey.", "আপনাদের গল্প, একটি সিনেমাটিক স্ক্রলিং যাত্রা।"),
      items=[("Personalized romantic website", "পার্সোনালাইজড রোমান্টিক ওয়েবসাইট"), ("Couple's story & memories", "কাপলের গল্প ও স্মৃতি"), ("Relationship timeline", "রিলেশনশিপ টাইমলাইন"), ("Personal photos", "ব্যক্তিগত ছবি"), ("Romantic messages", "রোমান্টিক বার্তা"), ("Cinematic scrolling", "সিনেমাটিক স্ক্রলিং"), ("Special emotional ending", "বিশেষ আবেগময় সমাপ্তি")],
      suit=("Couples who want to tell their story as a journey.", "যারা নিজেদের গল্পকে একটি যাত্রার মতো বলতে চান।")),
 dict(id="web-anniv", en="Premium Anniversary Website", bn="প্রিমিয়াম অ্যানিভার্সারি ওয়েবসাইট", price="1,799+", kind="from",
      deliv=("3–5 days", "৩–৫ দিন"), img="anniversary", pos="50% 50%", cls="s7 h",
      desc=("Our most elaborate romantic experience, with advanced animation.", "অ্যাডভান্সড অ্যানিমেশনসহ সবচেয়ে বিস্তারিত রোমান্টিক এক্সপেরিয়েন্স।"),
      items=[("Premium anniversary experience", "প্রিমিয়াম অ্যানিভার্সারি এক্সপেরিয়েন্স"), ("Personalized romantic homepage", "রোমান্টিক হোমপেজ"), ("Relationship timeline", "রিলেশনশিপ টাইমলাইন"), ("Memory gallery", "স্মৃতির গ্যালারি"), ("Special messages & letters", "বিশেষ বার্তা ও চিঠি"), ("Interactive surprise sections", "ইন্টারঅ্যাক্টিভ সারপ্রাইজ সেকশন"), ("Advanced animations", "অ্যাডভান্সড অ্যানিমেশন")],
      suit=("Anniversaries where you want the most elaborate experience.", "যে অ্যানিভার্সারিতে সবচেয়ে বিস্তারিত এক্সপেরিয়েন্স চান।")),
 dict(id="web-surprise", en="Custom Digital Surprise Website", bn="কাস্টম ডিজিটাল সারপ্রাইজ ওয়েবসাইট", price="699+", kind="from",
      deliv=("Depends on complexity", "প্রজেক্টের জটিলতা অনুযায়ী"), img="digital-surprise", pos="50% 50%", cls="s5",
      desc=("A website built around your own surprise idea.", "আপনার নিজের সারপ্রাইজ আইডিয়া নিয়ে তৈরি ওয়েবসাইট।"),
      items=[("Custom website from your idea", "আপনার আইডিয়ায় কাস্টম ওয়েবসাইট"), ("Interactive surprise elements", "ইন্টারঅ্যাক্টিভ সারপ্রাইজ"), ("Personalized messages", "পার্সোনালাইজড বার্তা"), ("Creative animations", "ক্রিয়েটিভ অ্যানিমেশন"), ("Custom sections", "কাস্টম সেকশন"), ("Special reveal or ending", "বিশেষ রিভিল বা সমাপ্তি")],
      suit=("Ideas that don't fit a standard package.", "যে আইডিয়া স্ট্যান্ডার্ড প্যাকেজে ধরে না।")),
]
for s in VIDEO: s["group"] = "video"
for s in WEB: s["group"] = "web"

def price_html(s):
    ke, kb = KIND[s["kind"]]
    return (f'<div class="price"><span class="p-label">{t(ke, kb)}</span>'
            f'<span class="p-val"><span class="cur">৳</span>{s["price"]}</span></div>')

def when(s):
    return s["dur"] if s["group"] == "video" else s["deliv"]

def when_label(s):
    return ("Duration", "সময়কাল") if s["group"] == "video" else ("Delivery", "ডেলিভারি")

def fb_btn(label_en, label_bn, cls="btn btn-gold", extra=""):
    return f'<a class="{cls}" href="{FB}" {REL} {extra}>{t(label_en, label_bn)}{ICON["arrow"]}</a>'

def svc_card(s, i):
    wl = when_label(s)
    horizontal = " h" if "h" in s["cls"].split() else ""
    span = s["cls"].split()[0]
    tagcls = "tag fixed" if s["kind"] == "fixed" else "tag"
    return f'''<article class="svc {span}{horizontal}" data-tilt data-rv>
  <div class="glare"></div>
  <div class="media shimmer"><img src="assets/img/{s["img"]}-sm.webp" alt="" loading="lazy" decoding="async" style="--pos:{s["pos"]}" onload="this.parentNode.classList.remove('shimmer')"><span class="tag">{t(*KIND[s["kind"]])}</span></div>
  <div class="body">
    <h4>{t(s["en"], s["bn"])}</h4>
    <p class="desc">{t(*s["desc"])}</p>
    <div class="meta"><span>{ICON["clock"]}{t(*wl)}: {t(*when(s))}</span></div>
    <div class="svc-foot">{price_html(s)}
      <div class="actions"><button class="btn btn-line btn-sm" type="button" data-svc="{s["id"]}" aria-haspopup="dialog">{t("Details", "বিস্তারিত")}</button>
      <a class="btn btn-gold btn-sm" href="{FB}" {REL}>{t("Order on Facebook", "ফেসবুকে অর্ডার")}</a></div>
    </div>
  </div>
</article>'''

def menu_row(s):
    wl = when_label(s)
    inc = "".join(f"<li>{t(a, b)}</li>" for a, b in s["items"][:3])
    return f'''<div class="menu-row" data-rv>
  <div class="nm"><h4>{t(s["en"], s["bn"])}</h4><span class="tag {"fixed" if s["kind"]=="fixed" else ""}">{t(*KIND[s["kind"]])}</span></div>
  <div class="when"><b>{t(*wl)}</b><span>{t(*when(s))}</span></div>
  <ul class="inc">{inc}</ul>
  {price_html(s)}
  <div class="go"><a class="btn btn-line btn-sm" href="{FB}" {REL}>{t("Order on Facebook", "ফেসবুকে অর্ডার")}</a></div>
</div>'''

# Portfolio: real sample videos from the existing project + clearly labelled concept artwork
PF = [
 dict(k="cinematic", kind="video", id="cine1", title="Moonlit Forest", poster="media/cine1.jpg", src="media/cine1.mp4", cat=("AI Cinematic Video", "এআই সিনেমাটিক ভিডিও"), badge=("Sample", "স্যাম্পল"), cls=""),
 dict(k="animation", kind="video", id="room309", title="The Boy in Room 309", poster="media/room309.jpg", src="media/room309.mp4", cat=("Stickman Animation", "স্টিকম্যান অ্যানিমেশন"), badge=("Sample", "স্যাম্পল"), cls="tall", portrait=True),
 dict(k="birthday", kind="concept", id="c-bday", title="Golden Birthday", img="birthday", cat=("Birthday Website", "বার্থডে ওয়েবসাইট"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept for a birthday website: warm gold, confetti and a cake that waits for the candles.", "জন্মদিনের ওয়েবসাইটের একটি কনসেপ্ট: উষ্ণ সোনালি রং, কনফেটি আর মোমবাতির অপেক্ষায় থাকা কেক।")),
 dict(k="cinematic", kind="video", id="lasttime", title="The Last Time Revealed", poster="media/lasttime.jpg", src="media/lasttime.mp4", cat=("AI Cinematic Video", "এআই সিনেমাটিক ভিডিও"), badge=("Sample", "স্যাম্পল"), cls=""),
 dict(k="love", kind="concept", id="c-love", title="Under the Blossoms", img="love-story", cat=("Love Story Website", "লাভ স্টোরি ওয়েবসাইট"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept for a love story website: a scrolling journey of photographs and memories.", "লাভ স্টোরি ওয়েবসাইটের একটি কনসেপ্ট: ছবি ও স্মৃতির স্ক্রলিং যাত্রা।")),
 dict(k="animation", kind="video", id="thirdperson", title="The Third Person", poster="media/thirdperson.jpg", src="media/thirdperson.mp4", cat=("Stickman Animation", "স্টিকম্যান অ্যানিমেশন"), badge=("Sample", "স্যাম্পল"), cls="tall", portrait=True),
 dict(k="anniversary", kind="concept", id="c-anniv", title="Two Rings, One Story", img="anniversary", cat=("Anniversary Website", "অ্যানিভার্সারি ওয়েবসাইট"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept for an anniversary website: soft silk, white blooms and a timeline of shared years.", "অ্যানিভার্সারি ওয়েবসাইটের একটি কনসেপ্ট: নরম সিল্ক, সাদা ফুল আর একসাথে কাটানো বছরের টাইমলাইন।")),
 dict(k="cinematic", kind="video", id="cine3", title="The Lost Boy", poster="media/cine3.jpg", src="media/cine3.mp4", cat=("AI Cinematic Video", "এআই সিনেমাটিক ভিডিও"), badge=("Sample", "স্যাম্পল"), cls=""),
 dict(k="surprise", kind="concept", id="c-surprise", title="The Gift That Opens", img="digital-surprise", cat=("Digital Surprise", "ডিজিটাল সারপ্রাইজ"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept for a digital surprise: a reveal that opens when the person you love taps it.", "ডিজিটাল সারপ্রাইজের একটি কনসেপ্ট: প্রিয় মানুষটি ট্যাপ করলেই খুলে যাওয়া একটি রিভিল।")),
 dict(k="animation", kind="video", id="lasttree", title="The Last Tree", poster="media/lasttree.jpg", src="media/lasttree.mp4", cat=("Stickman Animation", "স্টিকম্যান অ্যানিমেশন"), badge=("Sample", "স্যাম্পল"), cls="tall", portrait=True),
 dict(k="animation", kind="concept", id="c-story", title="The Forest Light", img="animated-story", cat=("Animated Story", "অ্যানিমেটেড স্টোরি"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept for a custom animated story: a small character, a quiet forest and a spark of light.", "কাস্টম অ্যানিমেটেড স্টোরির একটি কনসেপ্ট: ছোট্ট একটি চরিত্র, শান্ত বন আর এক টুকরো আলো।")),
 dict(k="cinematic", kind="concept", id="c-castle", title="Castle Above the Clouds", img="ai-cinematic", cat=("Cinematic Video", "সিনেমাটিক ভিডিও"), badge=("Concept", "কনসেপ্ট"), cls="",
      about=("A concept frame for a cinematic video: a sunrise over a castle in the clouds.", "সিনেমাটিক ভিডিওর একটি কনসেপ্ট ফ্রেম: মেঘের ওপর দুর্গে সূর্যোদয়।")),
]

def pf_tile(p):
    cap = f'<div class="cap"><b>{html.escape(p["title"])}</b><span>{t(*p["cat"])}</span></div>'
    badge = f'<span class="badge">{t(*p["badge"])}</span>'
    if p["kind"] == "video":
        attrs = f'data-kind="video" data-src="{p["src"]}" data-poster="{p["poster"]}" data-portrait="{1 if p.get("portrait") else 0}"'
        img = f'<img src="{p["poster"]}" alt="{html.escape(p["title"])} — sample film preview" loading="lazy" decoding="async">'
        play = f'<span class="play">{ICON["play"]}</span>'
    else:
        attrs = f'data-kind="concept" data-img="assets/img/{p["img"]}.webp"'
        img = f'<img src="assets/img/{p["img"]}-sm.webp" alt="{html.escape(p["title"])} — concept artwork" loading="lazy" decoding="async">'
        play = ""
    extra = ""
    if p["kind"] == "concept":
        extra = f' data-about-en="{html.escape(p["about"][0])}" data-about-bn="{html.escape(p["about"][1])}"'
    return (f'<button type="button" class="pf {p["cls"]} shimmer" data-cat="{p["k"]}" data-title="{html.escape(p["title"])}" '
            f'data-label-en="{p["cat"][0]}" data-label-bn="{p["cat"][1]}" data-badge-en="{p["badge"][0]}" data-badge-bn="{p["badge"][1]}" {attrs}{extra} '
            f'aria-haspopup="dialog" aria-label="{html.escape(p["title"])}, {p["cat"][0]}, {p["badge"][0]}">{img}{badge}{play}{cap}</button>')

FILTERS = [("all", "All", "সব"), ("birthday", "Birthday", "বার্থডে"), ("love", "Love Story", "লাভ স্টোরি"), ("anniversary", "Anniversary", "অ্যানিভার্সারি"),
           ("surprise", "Digital Surprise", "ডিজিটাল সারপ্রাইজ"), ("animation", "Animation", "অ্যানিমেশন"), ("cinematic", "Cinematic Video", "সিনেমাটিক ভিডিও")]

# process journeys
VSTEPS = [
 ("Share Your Idea", "আপনার আইডিয়া জানান", "Tell us your idea, the occasion and who it is for on our Facebook page.", "আমাদের ফেসবুক পেজে আপনার আইডিয়া, উপলক্ষ আর কার জন্য, তা জানান।"),
 ("We Create Your Preview", "আমরা প্রিভিউ তৈরি করি", "We settle the concept and details, then create your video with a watermarked preview.", "কনসেপ্ট ও বিস্তারিত ঠিক করে আমরা ওয়াটারমার্কসহ প্রিভিউ তৈরি করি।"),
 ("Review & Approve", "রিভিউ ও অনুমোদন", "Watch the preview and tell us what you think.", "প্রিভিউ দেখে আপনার মতামত জানান।"),
 ("Pay & Receive Your Final Video", "পেমেন্ট ও ফাইনাল ভিডিও", "Happy with it? Make the payment. Once confirmed, we deliver the clean, high-quality video.", "পছন্দ হলে পেমেন্ট করুন। নিশ্চিত হলে পরিষ্কার, হাই-কোয়ালিটি ভিডিও পাবেন।"),
]
WSTEPS = [
 ("Choose Your Experience", "আপনার এক্সপেরিয়েন্স বেছে নিন", "Pick the website that fits your occasion and your budget.", "উপলক্ষ ও বাজেট অনুযায়ী ওয়েবসাইট বেছে নিন।", "choose"),
 ("Share Your Details", "আপনার তথ্য দিন", "Send us the names, photos, messages and anything else you want included.", "নাম, ছবি, বার্তা ও আর যা যা চান, আমাদের পাঠান।", "details"),
 ("We Build Your Website", "আমরা ওয়েবসাইট তৈরি করি", "We design and build your personalized website to the agreed scope.", "সম্মত স্কোপ অনুযায়ী আপনার ওয়েবসাইট ডিজাইন ও তৈরি করি।", "build"),
 ("Receive Your Website Link", "ওয়েবসাইটের লিংক পান", "You receive a finished link, ready to share with someone special.", "প্রিয় মানুষকে পাঠানোর জন্য তৈরি একটি সম্পূর্ণ লিংক পাবেন।", "link"),
]
# circular crops of the process-icons artwork (bulb, wand, eye, gift): [x-position]
NODE_CX = [205, 520, 840, 1180]  # icon centres in process-icons.webp (px)

WHY = [
 ("heart", "Personalized creativity", "ব্যক্তিগত সৃজনশীলতা", "Every piece begins with your names, photos and memories, never a blank template.", "প্রতিটি কাজ শুরু হয় আপনার নাম, ছবি ও স্মৃতি দিয়ে, ফাঁকা টেমপ্লেট দিয়ে নয়।"),
 ("film", "Custom visual storytelling", "কাস্টম ভিজ্যুয়াল স্টোরিটেলিং", "Scenes, characters and pacing shaped around the story you want to tell.", "আপনার বলতে চাওয়া গল্প অনুযায়ী সাজানো দৃশ্য, চরিত্র ও গতি।"),
 ("eye", "Attention to detail", "খুঁটিনাটিতে মনোযোগ", "Small touches in light, type and motion are what make something feel crafted.", "আলো, লেখা ও গতির ছোট ছোট ছোঁয়াই কাজটিকে যত্নে গড়া করে তোলে।"),
 ("frame", "Creative presentation", "সৃজনশীল উপস্থাপনা", "A gift deserves a beautiful reveal, so the way it arrives matters as much as what it holds.", "উপহারের জন্য সুন্দর উন্মোচন দরকার; কী আছে, তার মতোই গুরুত্বপূর্ণ কীভাবে পৌঁছাচ্ছে।"),
 ("spark", "Memorable digital experiences", "স্মরণীয় ডিজিটাল অভিজ্ঞতা", "Videos and websites made to be opened, shared and remembered.", "খোলা, শেয়ার করা আর মনে রাখার জন্য তৈরি ভিডিও ও ওয়েবসাইট।"),
 ("check", "Thoughtful project execution", "সুচিন্তিত প্রজেক্ট বাস্তবায়ন", "A clear process from first idea to final delivery, with prices shown openly.", "প্রথম আইডিয়া থেকে ফাইনাল ডেলিভারি পর্যন্ত স্পষ্ট প্রক্রিয়া, মূল্য খোলাখুলি দেখানো।"),
]

NAV = [("home", "Home", "হোম"), ("services", "Services", "সার্ভিস"), ("portfolio", "Portfolio", "পোর্টফোলিও"), ("pricing", "Pricing", "প্রাইসিং"),
       ("about", "About", "আমাদের সম্পর্কে"), ("how", "How It Works", "কীভাবে কাজ করে"), ("contact", "Contact", "যোগাযোগ")]

# JSON handed to the browser for the service-detail dialog
SVC_JSON = {}
for s in VIDEO + WEB:
    SVC_JSON[s["id"]] = dict(
        name=[s["en"], s["bn"]], desc=list(s["desc"]), items=[list(i) for i in s["items"]], suit=list(s["suit"]),
        kind=list(KIND[s["kind"]]), price=s["price"], img=f'assets/img/{s["img"]}.webp',
        whenLabel=list(when_label(s)), when=list(when(s)), video=s["group"] == "video")

# ---------------------------------------------------------------- PAGE
def build_index():
    nav_links = "".join(f'<a href="#{i}" data-nav="{i}">{t(e, b)}</a>' for i, e, b in NAV)
    m_links = "".join(f'<a class="mlink" href="#{i}"><span>{t(e, b)}</span><small>0{n+1}</small></a>' for n, (i, e, b) in enumerate(NAV))
    foot_links = "".join(f'<li><a href="#{i}">{t(e, b)}</a></li>' for i, e, b in NAV)
    vcards = "".join(svc_card(s, i) for i, s in enumerate(VIDEO))
    wcards = "".join(svc_card(s, i) for i, s in enumerate(WEB))
    vrows = "".join(menu_row(s) for s in VIDEO)
    wrows = "".join(menu_row(s) for s in WEB)
    filters = "".join(f'<button type="button" class="chip" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t(e, b)}</button>' for k, e, b in FILTERS)
    tiles = "".join(pf_tile(p) for p in PF)
    band = "".join(t(x, y) and f'<span>{t(x, y)}</span>' for x, y in [("Dream", "স্বপ্ন"), ("Create", "সৃষ্টি"), ("Celebrate", "উদযাপন"), ("Stories Made Personal", "Stories Made Personal")]) * 4

    vsteps = ""
    for n, (e, b, de, db) in enumerate(VSTEPS):
        vsteps += f'''<div class="step" data-rv><div class="node img" style="--cx:{NODE_CX[n]};--cy:350" role="img" aria-label="{e}"></div><span class="n">{n+1:02d}</span><div><h4>{t(e, b)}</h4><p>{t(de, db)}</p></div></div>'''
    wsteps = ""
    for n, (e, b, de, db, ic) in enumerate(WSTEPS):
        wsteps += f'''<div class="step" data-rv><div class="node" aria-hidden="true">{ICON[ic]}</div><span class="n">{n+1:02d}</span><div><h4>{t(e, b)}</h4><p>{t(de, db)}</p></div></div>'''

    why = "".join(f'<div class="wcard" data-rv><div class="ic">{ICON[ic]}</div><h4>{t(e, b)}</h4><p>{t(de, db)}</p></div>' for ic, e, b, de, db in WHY)
    svc_opts = "".join(f'<option value="{html.escape(s["en"])}">{html.escape(s["en"])}</option>' for s in VIDEO + WEB)

    pay_steps = [
     ("We create the requested video.", "আপনার অনুরোধ করা ভিডিও আমরা তৈরি করি।"),
     ("We send a preview with a <strong>large watermark</strong>.", "আমরা <strong>বড় ওয়াটারমার্কসহ</strong> একটি প্রিভিউ পাঠাই।"),
     ("You review the preview.", "আপনি প্রিভিউটি রিভিউ করেন।"),
     ("If you are satisfied, you make the payment.", "সন্তুষ্ট হলে আপনি পেমেন্ট করেন।"),
     ("After payment is confirmed, the <strong>watermark is removed</strong>.", "পেমেন্ট নিশ্চিত হলে <strong>ওয়াটারমার্ক সরিয়ে ফেলা হয়</strong>।"),
     ("The clean, high-quality video is delivered to you.", "পরিষ্কার, হাই-কোয়ালিটি ভিডিও আপনার কাছে পৌঁছে দেওয়া হয়।"),
    ]
    pay_li = "".join(f'<li data-rv><span>{t(a, b)}</span></li>' for a, b in pay_steps)

    ld = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Taleora Studio", "slogan": "Stories Made Personal.", "sameAs": [FB]}, ensure_ascii=False)
    title = "Taleora Studio | Stories Made Personal."
    desc = "Taleora Studio creates personalized cinematic AI videos, custom animations, birthday, love story and anniversary websites in Bangladesh. Prices in BDT."

    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Taleora Studio">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF8F3">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="assets/img/hero.webp" fetchpriority="high">
<script>/* set theme + language before first paint (no flash) */
(function(){{var d=document.documentElement;try{{var t=localStorage.getItem("taleora-theme");d.setAttribute("data-theme",t==="dark"?"dark":"light");var l=localStorage.getItem("taleora-lang");if(l==="bn")d.lang="bn";}}catch(e){{}}d.classList.add("js");if(matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("reduced");}})();
</script>
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{t("Skip to content", "মূল অংশে যান")}</a>

<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="#home" aria-label="Taleora Studio — home"><b>Taleora</b><small>STUDIO</small></a>
    <nav class="links" aria-label="Main">{nav_links}</nav>
    <div class="tools">
      <button class="pill" id="lang" type="button" aria-label="Switch language / ভাষা বদলান"><b class="en">বাংলা</b><b class="bn">EN</b></button>
      <button class="icon-btn theme-toggle" id="theme" type="button" aria-label="Toggle light and dark theme" aria-pressed="false">{ICON["sun"]}{ICON["moon"]}</button>
      <a class="pill fb-link" href="{FB}" {REL} aria-label="Taleora Studio on Facebook">{ICON["fb"]}<span>Facebook</span></a>
      <button class="icon-btn burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mmenu" id="mmenu" aria-hidden="true">{m_links}<div class="row"><a class="btn btn-gold" href="{FB}" {REL}>{t("Visit Our Facebook Page", "আমাদের ফেসবুক পেজ")}{ICON["arrow"]}</a></div></div>

<main id="main">

<!-- HERO -->
<section class="hero" id="home" aria-labelledby="hero-h">
  <div class="wrap">
    <div class="hero-copy">
      <div class="brandline"><span class="eyebrow">Taleora Studio</span><span class="note">Stories Made Personal.</span></div>
      <h1 id="hero-h" data-hero>{t("Turn Your Imagination Into Something <em class='gold'>Unforgettable.</em>", "আপনার কল্পনাকে করে তুলুন <em class='gold'>অবিস্মরণীয়।</em>")}</h1>
      <p class="lead" data-hero>{t("We transform your ideas, memories and emotions into personalized videos, animations and beautiful digital experiences.", "আপনার আইডিয়া, স্মৃতি ও অনুভূতিকে আমরা রূপ দিই পার্সোনালাইজড ভিডিও, অ্যানিমেশন ও সুন্দর ডিজিটাল অভিজ্ঞতায়।")}</p>
      <div class="row" data-hero>
        <a class="btn btn-gold" href="#services">{t("Explore Our Services", "আমাদের সার্ভিস দেখুন")}{ICON["arrow"]}</a>
        <a class="btn btn-line" href="#portfolio">{t("Discover Our Creations", "আমাদের কাজ দেখুন")}</a>
      </div>
      <p class="phrase" data-hero><span>Dream</span><i></i><span>Create</span><i></i><span>Celebrate</span></p>
    </div>
    <div class="hero-visual" id="hero-visual" data-hero>
      <div class="hero-art"><img src="assets/img/hero.webp" alt="A couple sits on a floating island above the clouds, with film strips, photographs and a castle at sunset" width="1672" height="941" fetchpriority="high" decoding="async"></div>
      <canvas id="hero-gl" aria-hidden="true"></canvas>
      <figure class="mem m1" data-depth="26"><img src="media/cine1.jpg" alt="" loading="lazy" decoding="async"></figure>
      <figure class="mem m2" data-depth="40"><img src="media/room309.jpg" alt="" loading="lazy" decoding="async"></figure>
      <figure class="mem m3" data-depth="18"><img src="media/lasttime.jpg" alt="" loading="lazy" decoding="async"></figure>
      <div class="hero-chip"><i></i>{t("Personalized, from your story", "আপনার গল্প থেকে, আপনার জন্য")}</div>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true">SCROLL</div>
</section>

<div class="band" aria-hidden="true"><div class="track">{band}</div></div>

<!-- SERVICES -->
<section class="sec" id="services" aria-labelledby="services-h">
  <div class="wrap">
    <div class="sec-head" data-rv>
      <div><span class="eyebrow">{t("Services", "সার্ভিস")}</span><h2 id="services-h">{t("What We <em class='gold'>Create</em>", "আমরা যা <em class='gold'>তৈরি করি</em>")}</h2></div>
      <p class="lead">{t("Creative experiences designed around your most meaningful moments.", "আপনার সবচেয়ে অর্থপূর্ণ মুহূর্তগুলোকে ঘিরে সাজানো সৃজনশীল অভিজ্ঞতা।")}</p>
    </div>

    <div class="group" id="video-services">
      <div class="banner" data-rv><img src="assets/img/video-animation.webp" alt="A vintage film camera, reel and clapperboard in warm gold light" loading="lazy" decoding="async" data-parallax><span class="count">04 {t("services", "সার্ভিস")}</span></div>
      <div class="group-head" data-rv><h3>{t("Video &amp; Animation", "ভিডিও ও অ্যানিমেশন")}</h3><p>{t("Stories in motion, from a 30-second stickman tale to a one-minute animated story.", "গতিময় গল্প, ৩০ সেকেন্ডের স্টিকম্যান থেকে ১ মিনিটের অ্যানিমেটেড স্টোরি পর্যন্ত।")}</p></div>
      <div class="sgrid">{vcards}</div>
    </div>

    <div class="group" id="website-services">
      <div class="banner" data-rv><img src="assets/img/websites.webp" alt="A personalized website shown on a desktop, tablet and phone" loading="lazy" decoding="async" data-parallax style="object-position:50% 40%"><span class="count">05 {t("services", "সার্ভিস")}</span></div>
      <div class="group-head" data-rv><h3>{t("Personalized Websites", "পার্সোনালাইজড ওয়েবসাইট")}</h3><p>{t("A website made for one person, to open on any phone and share with a link.", "একজন মানুষের জন্য তৈরি ওয়েবসাইট, যেকোনো ফোনে খোলা যায়, লিংকে শেয়ার করা যায়।")}</p></div>
      <div class="sgrid">{wcards}</div>
    </div>
  </div>
</section>

<!-- PORTFOLIO -->
<section class="sec alt" id="portfolio" aria-labelledby="portfolio-h">
  <div class="wrap">
    <div class="sec-head" data-rv>
      <div><span class="eyebrow">{t("Portfolio", "পোর্টফোলিও")}</span><h2 id="portfolio-h">{t("Selected <em class='gold'>Creations</em>", "নির্বাচিত <em class='gold'>সৃষ্টি</em>")}</h2></div>
      <p class="lead">{t("A glimpse into our creative world.", "আমাদের সৃজনশীল জগতের এক ঝলক।")}</p>
    </div>
    <div class="filters" role="group" aria-label="Filter portfolio" data-rv>{filters}</div>
    <div class="pgrid" id="pgrid">{tiles}</div>
    <p class="note pf-note">{t("“Sample” tiles are example films you can watch. “Concept” tiles are design artwork that shows a direction, not completed customer projects.", "“স্যাম্পল” মানে দেখার মতো উদাহরণ ফিল্ম। “কনসেপ্ট” মানে একটি ডিজাইন-দিক দেখানো আর্টওয়ার্ক, সম্পন্ন কাস্টমার প্রজেক্ট নয়।")}</p>
  </div>
</section>

<!-- PRICING -->
<section class="sec" id="pricing" aria-labelledby="pricing-h">
  <div class="wrap">
    <div class="sec-head" data-rv>
      <div><span class="eyebrow">{t("Pricing", "প্রাইসিং")}</span><h2 id="pricing-h">{t("Clear, <em class='gold'>honest</em> pricing", "স্পষ্ট, <em class='gold'>খোলামেলা</em> মূল্য")}</h2></div>
      <p class="lead">{t("All prices are in Bangladeshi Taka (৳). Every service shows whether its price is fixed, a range, or a starting price.", "সব মূল্য বাংলাদেশি টাকায় (৳)। প্রতিটি সার্ভিসে দেখানো আছে মূল্য নির্দিষ্ট, পরিসর, নাকি শুরুর মূল্য।")}</p>
    </div>
    <div class="menu-group"><div class="menu-head" data-rv><h3>{t("Video &amp; Animation", "ভিডিও ও অ্যানিমেশন")}</h3></div><div class="menu">{vrows}</div></div>
    <div class="menu-group"><div class="menu-head" data-rv><h3>{t("Personalized Websites", "পার্সোনালাইজড ওয়েবসাইট")}</h3></div><div class="menu">{wrows}</div></div>
    <div class="price-note" data-rv>{ICON["info"]}<p>{t("<strong>Fixed price</strong> is a set amount. <strong>Starting price</strong> (or +) is where a service begins; the final amount depends on your idea. A <strong>price range</strong> depends on complexity. Full inclusions for each service are in its Details.", "<strong>নির্দিষ্ট মূল্য</strong> মানে ফিক্সড অঙ্ক। <strong>শুরুর মূল্য</strong> (বা +) মানে সার্ভিসটি এখান থেকে শুরু, চূড়ান্ত অঙ্ক আপনার আইডিয়ার ওপর নির্ভর করে। <strong>মূল্যের পরিসর</strong> নির্ভর করে জটিলতার ওপর। প্রতিটি সার্ভিসের পূর্ণ তালিকা “বিস্তারিত”-এ আছে।")}</p></div>
  </div>
</section>

<!-- ABOUT -->
<section class="sec alt" id="about" aria-labelledby="about-h">
  <div class="wrap about">
    <div class="about-art" data-rv>
      <div class="main"><img src="assets/img/about-studio.webp" alt="A creative studio with a cinema camera, film reels, storyboards and photographs floating in warm light" loading="lazy" decoding="async" data-parallax></div>
      <div class="quote"><p>{t("We don’t just create digital content. We turn personal stories into experiences.", "আমরা শুধু ডিজিটাল কনটেন্ট বানাই না। ব্যক্তিগত গল্পকে অভিজ্ঞতায় বদলে দিই।")}</p><small>Taleora Studio</small></div>
    </div>
    <div class="about-copy" data-rv>
      <span class="eyebrow">{t("About", "আমাদের সম্পর্কে")}</span>
      <h2 id="about-h">{t("Where memories become <em class='gold'>experiences</em>", "যেখানে স্মৃতি হয়ে ওঠে <em class='gold'>অভিজ্ঞতা</em>")}</h2>
      <p>{t("Taleora Studio is a personalized digital creative studio in Bangladesh. We turn ideas, memories and celebrations into cinematic AI videos, custom animations and websites made for one person.", "Taleora Studio বাংলাদেশের একটি পার্সোনালাইজড ডিজিটাল ক্রিয়েটিভ স্টুডিও। আমরা আইডিয়া, স্মৃতি ও উদযাপনকে সিনেমাটিক এআই ভিডিও, কাস্টম অ্যানিমেশন এবং একজন মানুষের জন্য তৈরি ওয়েবসাইটে রূপ দিই।")}</p>
      <p>{t("A birthday, an anniversary, a love story: these moments happen once, and a template cannot hold them. A story built around your names, your photos and your words can.", "জন্মদিন, বার্ষিকী, ভালোবাসার গল্প, এই মুহূর্তগুলো একবারই আসে, টেমপ্লেটে ধরে না। আপনার নাম, ছবি ও কথা দিয়ে গড়া গল্প তা ধরে রাখতে পারে।")}</p>
      <p>{t("Our commitment is thoughtful visual storytelling: careful detail, warm craft, and work that feels like a gift rather than a file.", "আমাদের প্রতিশ্রুতি সুচিন্তিত ভিজ্যুয়াল স্টোরিটেলিং: যত্নের খুঁটিনাটি, উষ্ণ কারুকাজ, আর এমন কাজ যা ফাইল নয়, উপহারের মতো লাগে।")}</p>
      <div class="dcc">
        <div><b>{t("Dream", "স্বপ্ন")}</b><span>{t("It starts with your idea, however small.", "শুরু আপনার আইডিয়া দিয়ে, তা যত ছোটই হোক।")}</span></div>
        <div><b>{t("Create", "সৃষ্টি")}</b><span>{t("We shape it into video, animation or a website.", "আমরা সেটিকে ভিডিও, অ্যানিমেশন বা ওয়েবসাইটে রূপ দিই।")}</span></div>
        <div><b>{t("Celebrate", "উদযাপন")}</b><span>{t("You share it with the person it was made for.", "যার জন্য তৈরি, তার সাথে ভাগ করে নেন।")}</span></div>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="sec" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="sec-head center" style="justify-content:center;text-align:center" data-rv>
      <div><span class="eyebrow">{t("How It Works", "কীভাবে কাজ করে")}</span><h2 id="how-h">{t("Two journeys, <em class='gold'>one</em> simple path", "দুটি যাত্রা, <em class='gold'>একটাই</em> সহজ পথ")}</h2><p class="lead">{t("Video orders and website orders follow separate processes.", "ভিডিও ও ওয়েবসাইট অর্ডারের প্রক্রিয়া আলাদা।")}</p></div>
    </div>
    <div class="journey" data-journey>
      <div class="j-head" data-rv><h3>{t("Video &amp; Animation", "ভিডিও ও অ্যানিমেশন")}</h3><span class="tag">{t("Pay after you approve the preview", "প্রিভিউ অনুমোদনের পর পেমেন্ট")}</span></div>
      <div class="steps"><span class="fill"></span>{vsteps}</div>
    </div>
    <div class="journey" data-journey>
      <div class="j-head" data-rv><h3>{t("Website Services", "ওয়েবসাইট সার্ভিস")}</h3></div>
      <div class="steps"><span class="fill"></span>{wsteps}</div>
      <p class="j-note" data-rv>{t("Payment, hosting and revision details for websites are confirmed with you directly.", "ওয়েবসাইটের পেমেন্ট, হোস্টিং ও রিভিশনের বিষয় সরাসরি আপনার সাথে নিশ্চিত করা হয়।")}</p>
    </div>
  </div>
</section>

<!-- PREVIEW & PAYMENT (video only) -->
<section class="sec zone-dark" id="preview-payment" aria-labelledby="pay-h">
  <div class="wrap pay">
    <div data-rv>
      <span class="eyebrow">{t("Video &amp; animation only", "শুধু ভিডিও ও অ্যানিমেশন")}</span>
      <h2 id="pay-h">{t("See it first. <em class='gold'>Pay</em> when you love it.", "আগে দেখুন। পছন্দ হলে <em class='gold'>পেমেন্ট</em>।")}</h2>
      <p class="lead" style="margin-top:18px">{t("You review a watermarked preview before any payment. Only after payment is confirmed do we remove the watermark and deliver the final video.", "পেমেন্টের আগে আপনি ওয়াটারমার্কসহ প্রিভিউ দেখেন। পেমেন্ট নিশ্চিত হলেই আমরা ওয়াটারমার্ক সরিয়ে ফাইনাল ভিডিও দিই।")}</p>
      <ol class="pay-list">{pay_li}</ol>
      <p class="pay-warn">{t("This workflow applies to video and animation services only. Website orders follow their own process above.", "এই ধাপগুলো শুধু ভিডিও ও অ্যানিমেশন সার্ভিসের জন্য। ওয়েবসাইট অর্ডারের প্রক্রিয়া ওপরে আলাদাভাবে দেওয়া আছে।")}</p>
    </div>
    <div data-rv>
      <div class="player" id="player"><img src="media/lasttime.jpg" alt="Example video frame" loading="lazy" decoding="async"><div class="wm" aria-hidden="true">{"<span>PREVIEW</span>"*9}</div><div class="stamp"><i></i><span id="stamp">{t("Preview with watermark", "ওয়াটারমার্কসহ প্রিভিউ")}</span></div></div>
      <div class="toggle" role="group" aria-label="Preview or final">
        <button type="button" data-state="preview" aria-pressed="true">{t("1 · Preview", "১ · প্রিভিউ")}</button>
        <button type="button" data-state="paid" aria-pressed="false">{t("2 · After payment", "২ · পেমেন্টের পর")}</button>
      </div>
      <p class="note" style="margin-top:12px">{t("Illustration of the process using one of our sample frames.", "আমাদের একটি স্যাম্পল ফ্রেম দিয়ে প্রক্রিয়ার ব্যাখ্যা।")}</p>
    </div>
  </div>
</section>

<!-- WHY -->
<section class="sec" id="why" aria-labelledby="why-h">
  <div class="wrap">
    <div class="sec-head" data-rv>
      <div><span class="eyebrow">{t("Why Taleora Studio", "কেন Taleora Studio")}</span><h2 id="why-h">{t("Made with <em class='gold'>care</em>, made for you", "যত্নে গড়া, <em class='gold'>আপনার</em> জন্য")}</h2></div>
      <p class="lead">{t("What you can expect when you work with us.", "আমাদের সাথে কাজ করলে যা আশা করতে পারেন।")}</p>
    </div>
    <div class="why">{why}</div>
  </div>
</section>

<!-- CONTACT -->
<section class="sec zone-dark" id="contact" aria-labelledby="contact-h">
  <div class="wrap contact">
    <div data-rv>
      <span class="eyebrow">{t("Contact", "যোগাযোগ")}</span>
      <h2 id="contact-h">{t("Let’s make it <em class='gold'>personal.</em>", "চলুন গল্পটা <em class='gold'>আপনার</em> করে তুলি।")}</h2>
      <p class="lead">{t("Tell us your idea on our official Facebook page. We’ll talk through your story, the right service and the next steps together.", "আমাদের অফিসিয়াল ফেসবুক পেজে আপনার আইডিয়া জানান। আপনার গল্প, সঠিক সার্ভিস ও পরের ধাপ নিয়ে আমরা একসাথে কথা বলব।")}</p>
      <div class="row"><a class="btn btn-gold" href="{FB}" {REL}>{ICON["fb"]}{t("Visit Our Facebook Page", "আমাদের ফেসবুক পেজে যান")}</a></div>
      <div class="contact-art"><img src="assets/img/digital-surprise.webp" alt="An ornate gift box opening with golden light, ribbons and butterflies" loading="lazy" decoding="async"></div>
    </div>
    <form class="planner" id="planner" data-rv onsubmit="return false" novalidate>
      <h3>{t("Prepare your message", "আপনার বার্তা গুছিয়ে নিন")}</h3>
      <p class="note">{t("This form does not send or submit anything. It only helps you write a clear first message to copy and paste to us on Facebook.", "এই ফর্ম কিছুই পাঠায় না বা জমা দেয় না। শুধু ফেসবুকে কপি-পেস্ট করার জন্য একটি পরিষ্কার প্রথম বার্তা লিখতে সাহায্য করে।")}</p>
      <div class="f2"><div class="f"><label for="pl-name">{t("Your name", "আপনার নাম")}</label><input id="pl-name" autocomplete="name"></div>
      <div class="f"><label for="pl-date">{t("Needed by (optional)", "কবে দরকার (ঐচ্ছিক)")}</label><input id="pl-date" type="date"></div></div>
      <div class="f"><label for="pl-svc">{t("Service", "সার্ভিস")}</label><select id="pl-svc"><option value="">—</option>{svc_opts}</select></div>
      <div class="f"><label for="pl-idea">{t("Your idea", "আপনার আইডিয়া")}</label><textarea id="pl-idea"></textarea></div>
      <div class="row"><button class="btn btn-gold" type="button" id="pl-copy">{t("Copy message", "বার্তা কপি করুন")}</button><a class="btn btn-line" href="{FB}" {REL}>{t("Open Facebook Page", "ফেসবুক পেজ খুলুন")}{ICON["arrow"]}</a></div>
      <p class="copied" id="pl-ok" role="status">{t("Copied. Paste it into a message on our Facebook page.", "কপি হয়েছে। আমাদের ফেসবুক পেজে বার্তায় পেস্ট করুন।")}</p>
      <p class="legal">{t("All orders and questions are handled through our official Facebook page only.", "সব অর্ডার ও প্রশ্ন শুধু আমাদের অফিসিয়াল ফেসবুক পেজের মাধ্যমে।")}</p>
    </form>
  </div>
</section>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="cols">
      <div><a class="logo" href="#home"><b>Taleora</b><small>STUDIO</small></a><p class="tagline">Stories Made Personal.</p><p class="note">Dream • Create • Celebrate</p></div>
      <div><h6>{t("Explore", "দেখুন")}</h6><ul>{foot_links}</ul></div>
      <div><h6>{t("Order &amp; contact", "অর্ডার ও যোগাযোগ")}</h6><ul><li><a href="{FB}" {REL}>{t("Official Facebook Page", "অফিসিয়াল ফেসবুক পেজ")}</a></li></ul><p class="note" style="margin-top:14px">{t("All orders and inquiries go through Facebook.", "সব অর্ডার ও জিজ্ঞাসা ফেসবুকের মাধ্যমে।")}</p></div>
    </div>
    <div class="bottom"><span>© 2026 Taleora Studio</span><span>{t("Prices in Bangladeshi Taka (৳)", "মূল্য বাংলাদেশি টাকায় (৳)")}</span></div>
  </div>
</footer>

<button class="to-top" id="to-top" type="button" aria-label="Back to top">{ICON["up"]}</button>

<!-- service detail dialog -->
<dialog id="svc-dlg" aria-labelledby="svc-title"><div class="dlg">
  <button class="dlg-x" type="button" data-close aria-label="Close">{ICON["x"]}</button>
  <div class="dlg-split">
    <div class="dlg-media"><img id="svc-img" src="" alt=""></div>
    <div class="dlg-body">
      <div><span class="tag" id="svc-kind"></span></div>
      <h3 id="svc-title"></h3>
      <p class="lead" id="svc-desc" style="font-size:1rem"></p>
      <div class="dlg-facts"><div id="svc-price"></div><div class="price"><span class="p-label" id="svc-wl"></span><span class="p-val" style="font-size:1.35rem;line-height:2.2rem" id="svc-w"></span></div></div>
      <div class="dlg-sec"><h5>{t("What you receive", "যা পাবেন")}</h5><ul id="svc-items"></ul></div>
      <div class="dlg-sec"><h5>{t("Suitable for", "যাদের জন্য")}</h5><p id="svc-suit"></p></div>
      <div class="dlg-sec"><h5>{t("How to order", "কীভাবে অর্ডার করবেন")}</h5><ol class="how-order" id="svc-order"></ol></div>
      <div class="row"><a class="btn btn-gold" href="{FB}" {REL}>{t("Order on Facebook", "ফেসবুকে অর্ডার করুন")}{ICON["arrow"]}</a></div>
    </div>
  </div>
</div></dialog>

<!-- portfolio dialog -->
<dialog id="pf-dlg" aria-labelledby="pf-title"><div class="dlg vid" id="pf-box">
  <button class="dlg-x" type="button" data-close aria-label="Close">{ICON["x"]}</button>
  <div class="dlg-video" id="pf-video"><video id="pf-player" controls playsinline preload="none"></video></div>
  <div class="dlg-split" id="pf-concept" hidden><div class="dlg-media"><img id="pf-img" src="" alt=""></div><div class="dlg-body" style="justify-content:center"></div></div>
  <div class="cp" id="pf-cap" style="padding:20px 26px;display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap"><div><span class="tag" id="pf-badge"></span><h3 id="pf-title" style="font-size:1.8rem;margin-top:8px"></h3><p class="note" id="pf-sub"></p></div><a class="btn btn-gold" href="{FB}" {REL}>{t("Ask about this on Facebook", "এ নিয়ে ফেসবুকে জানুন")}{ICON["arrow"]}</a></div>
</div></dialog>

<script type="application/json" id="svc-data">{json.dumps(SVC_JSON, ensure_ascii=False)}</script>
<script src="assets/vendor/gsap.min.js" defer></script>
<script src="assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="assets/js/app.js" defer></script>
</body>
</html>
'''

def redirect(target, label):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{label} | Taleora Studio</title><meta http-equiv="refresh" content="0;url=index.html#{target}"><link rel="canonical" href="index.html#{target}">
<script>location.replace("index.html#{target}")</script></head><body><p><a href="index.html#{target}">Continue to Taleora Studio</a></p></body></html>'''

if __name__ == "__main__":
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    # legacy routes from the previous multi-page site keep working
    for fn, target, label in [("services.html", "services", "Services"), ("pricing.html", "pricing", "Pricing"), ("portfolio.html", "portfolio", "Portfolio"),
                              ("how-it-works.html", "how", "How It Works"), ("about.html", "about", "About"), ("contact.html", "contact", "Contact")]:
        with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
            f.write(redirect(target, label))
    print("built")
