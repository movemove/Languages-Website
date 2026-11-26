#!/usr/bin/env python3
"""Build 6-language AE Travel Language Portal showcase, /privacy, and /support pages, and deploy to https://languages.appengine.fun."""
from __future__ import annotations

import argparse
import base64
import html as html_mod
import json
import os
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
IMG_DIR = PUBLIC_DIR / "images"
AUD_DIR = PUBLIC_DIR / "audio"

ACCOUNT_ID = "9fb3b494e6d4d659f2cf567efb94fc38"
ZONE_ID = "977b0b4fa0ab6e587b8758a04016c5e8"
SCRIPT_NAME = "languages-site"
HOSTNAME = "languages.appengine.fun"
ORIGIN = f"https://{HOSTNAME}"

LANG_ORDER = ("en", "zh-Hant", "zh-Hans", "ja", "ko", "es")
LANG_LABELS = [
    ("en", "EN"),
    ("zh-Hant", "繁中"),
    ("zh-Hans", "简中"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("es", "ES"),
]

APPS = [
    {
        "slug": "nihongo",
        "name": "NihonGo",
        "accent": "#818CF8",
        "accent_soft": "rgba(129, 140, 248, 0.16)",
        "flag": "🇯🇵",
        "app_store_id": "6836279889",
        "app_store_url": "https://apps.apple.com/app/id6836279889",
        "website_url": "https://nihongo.appengine.fun",
        "version": "1.2.0",
        "title": {
            "en": "NihonGo — Japanese",
            "zh-Hant": "NihonGo — 旅遊日語",
            "zh-Hans": "NihonGo — 旅游日语",
            "ja": "NihonGo — 旅行日本語",
            "ko": "NihonGo — 여행 일본어",
            "es": "NihonGo — Japonés de Viaje",
        },
        "pill_label": {
            "en": "Japanese · NihonGo",
            "zh-Hant": "日語 · NihonGo",
            "zh-Hans": "日语 · NihonGo",
            "ja": "日本語 · NihonGo",
            "ko": "일본어 · NihonGo",
            "es": "Japonés · NihonGo",
        },
        "tagline": {
            "en": "104 Kana with stroke tracing, 100 Tokyo travel video dialogues, 12 roleplay scenes & 2-way voice interpreter.",
            "zh-Hant": "104 五十音筆順手寫、100 部東京實境對話影片、12 情境口說與雙向即時語音口譯。",
            "zh-Hans": "104 五十音笔顺手写、100 部东京实景对话视频、12 情景口语与双向实时语音口译。",
            "ja": "104かな手書き練習、東京実境会話動画100本、12場面ロールプレイ＆双方向音声通訳。",
            "ko": "104 가나 필순 쓰기, 도쿄 실전 회화 영상 100편, 12장면 말하기 연습 및 양방향 통역.",
            "es": "104 Kana con trazos, 100 vídeos reales en Tokio, 12 escenas orales e intérprete de voz.",
        },
        "specs": {
            "en": ["104 Hiragana & Katakana + Tracing", "15 Guided Units · 18 Drills", "100 Japan Video Dialogues", "160 SM-2 Flashcards · v1.2.0"],
            "zh-Hant": ["104 平假名／片假名＋手寫筆順", "15 堂系統課 · 18 文法特訓", "100 部日本實境對話影片", "160 張 SRS 單字卡 · v1.2.0"],
            "zh-Hans": ["104 平假名／片假名＋手写笔顺", "15 节系统课 · 18 语法特训", "100 部日本实景对话视频", "160 张 SRS 词卡 · v1.2.0"],
            "ja": ["104 ひらがな・カタカナ筆順", "全15課 · 助詞・敬語ドリル18問", "実境旅行動画100本収録", "SM-2単語帳160語 · v1.2.0"],
            "ko": ["104 히라가나·가타카나 필순", "15개 핵심 유닛 · 문법 18개", "일본 현지 회화 영상 100편", "SM-2 단어장 160개 · v1.2.0"],
            "es": ["104 Hiragana y Katakana + trazos", "15 unidades · 18 ejercicios", "100 vídeos de viaje en Japón", "160 tarjetas SRS · v1.2.0"],
        },
        "script_col": {
            "en": "104 Kana + Stroke Canvas",
            "zh-Hant": "104 五十音＋手寫筆順",
            "zh-Hans": "104 五十音＋手写笔顺",
            "ja": "104かな＋筆順キャンバス",
            "ko": "104 가나＋필순 쓰기",
            "es": "104 Kana + lienzo trazos",
        },
        "highlight_col": {
            "en": "Particle-aware Romaji (wa / o / e)",
            "zh-Hant": "助詞變音標註 (は→wa / へ→e)",
            "zh-Hans": "助词变音标注 (は→wa / へ→e)",
            "ja": "助詞発音ガイド (は→wa / へ→e)",
            "ko": "조사 발음 표시 (は→wa / へ→e)",
            "es": "Romaji con partículas (wa/o/e)",
        },
        "audios": [
            {
                "id": "jp_split",
                "file": "jp_split.mp3",
                "phrase": "お会計は別々でお願いします。",
                "phonetic": "o kaikei <b>wa</b> betsubetsu de o negai shi masu",
                "meaning": {
                    "en": "Separate checks, please.",
                    "zh-Hant": "結帳麻煩分開算。",
                    "zh-Hans": "结账麻烦分开算。",
                    "ja": "別々にお会計をお願いする表現。",
                    "ko": "계산은 따로 부탁드립니다.",
                    "es": "La cuenta por separado, por favor.",
                },
                "tag": {
                    "en": "Izakaya · Particle ha → wa",
                    "zh-Hant": "居酒屋 · 助詞は→wa",
                    "zh-Hans": "居酒屋 · 助词は→wa",
                    "ja": "居酒屋 · 助詞は→wa",
                    "ko": "이자카야 · 조사 は→wa",
                    "es": "Izakaya · Partícula wa",
                },
            },
            {
                "id": "jp_wait",
                "file": "jp_wait.mp3",
                "phrase": "すみません、ちょっと待ってください。",
                "phonetic": "sumimasen, chotto matte kudasai",
                "meaning": {
                    "en": "Excuse me, please wait a moment.",
                    "zh-Hant": "不好意思，請稍等一下。",
                    "zh-Hans": "不好意思，请稍等一下。",
                    "ja": "お店や駅で「少し待ってください」。",
                    "ko": "실례지만 잠깐만 기다려 주세요.",
                    "es": "Disculpe, espere un momento.",
                },
                "tag": {
                    "en": "Counter Polite Essential",
                    "zh-Hant": "店鋪必備禮貌句",
                    "zh-Hans": "店铺必备礼貌句",
                    "ja": "お店・駅で使える定番表現",
                    "ko": "매장 필수 예의 표현",
                    "es": "Frase clave en tienda",
                },
            },
        ],
    },
    {
        "slug": "englishgo",
        "name": "EnglishGo",
        "accent": "#38BDF8",
        "accent_soft": "rgba(56, 189, 248, 0.16)",
        "flag": "🇺🇸",
        "app_store_id": "6837609680",
        "app_store_url": "https://apps.apple.com/app/id6837609680",
        "website_url": "https://englishgo.appengine.fun",
        "version": "1.0.0",
        "title": {
            "en": "EnglishGo — Travel English",
            "zh-Hant": "EnglishGo — 旅遊英語",
            "zh-Hans": "EnglishGo — 旅游英语",
            "ja": "EnglishGo — 旅行英語",
            "ko": "EnglishGo — 여행 영어",
            "es": "EnglishGo — Inglés de Viaje",
        },
        "pill_label": {
            "en": "English · EnglishGo",
            "zh-Hant": "英語 · EnglishGo",
            "zh-Hans": "英语 · EnglishGo",
            "ja": "英語 · EnglishGo",
            "ko": "영어 · EnglishGo",
            "es": "Inglés · EnglishGo",
        },
        "tagline": {
            "en": "44 US & UK IPA phonemes, 24 minimal-pair ear drills, 100 real travel videos, and live 2-way voice interpreter.",
            "zh-Hant": "44 個美式／英式音標與嘴型圖、24 組最小對立對辨音、100 部實境影片與雙向口譯。",
            "zh-Hans": "44 个美式／英式音标与口型图、24 组最小对立对辨音、100 部实景视频与双向口译。",
            "ja": "米英44 IPA発音記号、24組の聞き分けテスト、旅行動画100本＆双方向音声通訳。",
            "ko": "미국·영국식 44 IPA 발음 기호, 24쌍 듣기 훈련, 실전 영상 100편 및 실시간 통역.",
            "es": "44 fonemas IPA US/UK, 24 pares mínimos auditivos, 100 vídeos reales e intérprete en vivo.",
        },
        "specs": {
            "en": ["44 US & UK IPA Phonemes + 24 Pairs", "15 Guided Units · 18 Grammar Drills", "100 Real Travel Dialogues", "160 SRS Flashcards · 320 Clips"],
            "zh-Hant": ["44 美英雙音標＋24 組辨音挑戰", "15 堂系統課 · 18 堂文法", "100 部海外自由行實境短片", "160 單字卡 · 320 句原生錄音"],
            "zh-Hans": ["44 美英双音标＋24 组辨音挑战", "15 节系统课 · 18 节语法", "100 部海外自由行实景短片", "160 词卡 · 320 句原生录音"],
            "ja": ["米英44 IPA記号＋24組聞き分け", "全15課 · 文法クイズ18問", "実境トラベル動画100本", "SM-2単語帳160語 · 音声320本"],
            "ko": ["44개 미국/영국 IPA + 24쌍 훈련", "15개 유닛 · 문법 18개", "해외여행 실전 영상 100편", "SM-2 카드 160장 · 오디오 320개"],
            "es": ["44 fonemas IPA US/UK + 24 pares", "15 unidades · 18 ejercicios", "100 vídeos reales de viaje", "160 tarjetas SRS · 320 audios"],
        },
        "script_col": {
            "en": "44 US/UK IPA + 24 Pairs",
            "zh-Hant": "44 美英 IPA＋24 辨音",
            "zh-Hans": "44 美英 IPA＋24 辨音",
            "ja": "米英44 IPA＋24組聞き分け",
            "ko": "44 US/UK IPA＋24쌍",
            "es": "44 IPA US/UK + 24 pares",
        },
        "highlight_col": {
            "en": "US vs. UK accent & ship/sheep drills",
            "zh-Hant": "美式／英式音標切換＋ship/sheep 盲測",
            "zh-Hans": "美式／英式音标切换＋ship/sheep 盲测",
            "ja": "米語/英語IPA切替＆聞き分け",
            "ko": "미국/영국 발음 비교 및 최소대립쌍",
            "es": "Guía IPA US/UK y pares ship/sheep",
        },
        "audios": [
            {
                "id": "en_card",
                "file": "en_card.mp3",
                "phrase": "Do you take credit cards or Apple Pay?",
                "phonetic": "/duː juː teɪk <b>ˈkrɛdɪt kɑːrdz</b> ɔːr ˈæpəl peɪ/",
                "meaning": {
                    "en": "Checking accepted payment methods at checkout.",
                    "zh-Hant": "請問你們收信用卡或 Apple Pay 嗎？",
                    "zh-Hans": "请问你们收信用卡或 Apple Pay 吗？",
                    "ja": "クレジットカードかApple Payは使えますか？",
                    "ko": "신용카드나 애플페이 결제 되나요?",
                    "es": "¿Aceptan tarjetas de crédito o Apple Pay?",
                },
                "tag": {
                    "en": "Café & Shop · Payment",
                    "zh-Hant": "咖啡廳結帳 · 付款方式",
                    "zh-Hans": "咖啡厅结账 · 付款方式",
                    "ja": "カフェ・買い物 · お支払い",
                    "ko": "카페·매장 · 결제",
                    "es": "Cafetería · Pagos",
                },
            },
            {
                "id": "en_bill",
                "file": "en_bill.mp3",
                "phrase": "Excuse me, could we get the check?",
                "phonetic": "/ɪkˈskjuːz miː kʊd wiː ɡɛt ðə <b>tʃɛk</b>/",
                "meaning": {
                    "en": "Asking politely for the restaurant bill.",
                    "zh-Hant": "不好意思，請問可以結帳嗎？",
                    "zh-Hans": "不好意思，请问可以结账吗？",
                    "ja": "すみません、お会計をお願いできますか？",
                    "ko": "실례합니다, 계산서 좀 주시겠어요?",
                    "es": "Disculpe, ¿nos trae la cuenta?",
                },
                "tag": {
                    "en": "Dining · Check vs. Bill",
                    "zh-Hant": "餐廳結帳 · Check / Bill",
                    "zh-Hans": "餐厅结账 · Check / Bill",
                    "ja": "レストラン会計 · check / bill",
                    "ko": "식당 계산 · Check / Bill",
                    "es": "Restaurante · La cuenta",
                },
            },
        ],
    },
    {
        "slug": "espanolgo",
        "name": "EspanolGo",
        "accent": "#FB7185",
        "accent_soft": "rgba(251, 113, 133, 0.16)",
        "flag": "🇪🇸",
        "app_store_id": "6837611917",
        "app_store_url": "https://apps.apple.com/app/id6837611917",
        "website_url": "https://espanolgo.appengine.fun",
        "version": "1.0.0",
        "title": {
            "en": "EspanolGo — Spanish",
            "zh-Hant": "EspanolGo — 旅遊西語",
            "zh-Hans": "EspanolGo — 旅游西语",
            "ja": "EspanolGo — 旅行スペイン語",
            "ko": "EspanolGo — 여행 스페인어",
            "es": "EspanolGo — Español de Viaje",
        },
        "pill_label": {
            "en": "Spanish · EspanolGo",
            "zh-Hant": "西語 · EspanolGo",
            "zh-Hans": "西语 · EspanolGo",
            "ja": "スペイン語 · EspanolGo",
            "ko": "스페인어 · EspanolGo",
            "es": "Español · EspanolGo",
        },
        "tagline": {
            "en": "32 LatAm & España sound rules, 24 minimal pairs (pero/perro), 100 real travel videos & live 2-way interpreter.",
            "zh-Hant": "32 個拉美／西班牙發音規則、24 組彈舌與喉音辨音、100 部實境影片與雙向口譯。",
            "zh-Hans": "32 个拉美／西班牙发音规则、24 组大舌音与喉音辨音、100 部实景视频与双向口译。",
            "ja": "中南米/スペイン対応32音声ルール、24組聞き分け、動画100本＆双方向音声通訳。",
            "ko": "중남미·스페인식 32 발음 규칙, 24쌍 최소대립쌍, 회화 영상 100편 및 실시간 통역.",
            "es": "32 reglas fonéticas LatAm/España, 24 pares mínimos, 100 vídeos reales e intérprete en vivo.",
        },
        "specs": {
            "en": ["32 LatAm/España Sounds + 24 Pairs", "15 Guided Units · 18 Drills", "100 Real Travel Videos (200 MP3s)", "160 SM-2 Flashcards · 320 Clips"],
            "zh-Hant": ["32 拉美／西班牙音標＋24 組辨音", "15 堂旅遊課 · 18 文法測驗", "100 部西語實境短片（200 音檔）", "160 SRS 單字卡 · 320 句錄音"],
            "zh-Hans": ["32 拉美／西班牙音标＋24 组辨音", "15 节旅游课 · 18 语法测验", "100 部西语实景短片（200 音频）", "160 SRS 词卡 · 320 句录音"],
            "ja": ["32音声ルール＋24組聞き分け", "全15課 · 文法ドリル18問", "実境会話動画100本（音声200本）", "160語SM-2単語帳 · 音声320本"],
            "ko": ["32 발음 규칙＋24쌍 듣기 훈련", "15개 유닛 · 문법 드릴 18개", "스페인어 회화 영상 100편", "160 단어 카드 · 오디오 320개"],
            "es": ["32 sonidos LatAm/España + 24 pares", "15 unidades · 18 ejercicios", "100 vídeos reales (200 audios)", "160 tarjetas SRS · 320 audios"],
        },
        "script_col": {
            "en": "32 Sounds + 24 Pairs",
            "zh-Hant": "32 西語音標＋24 辨音",
            "zh-Hans": "32 西语音标＋24 辨音",
            "ja": "32音声ルール＋24組",
            "ko": "32 음운 규칙＋24쌍",
            "es": "32 sonidos + 24 pares",
        },
        "highlight_col": {
            "en": "LatAm Seseo vs. España Distinción + R/RR",
            "zh-Hant": "拉美/西班牙咬舌音比較＋大舌音 r/rr",
            "zh-Hans": "拉美/西班牙咬舌音对比＋大舌音 r/rr",
            "ja": "中南米/スペイン発音差＆巻き舌 r/rr",
            "ko": "중남미/스페인 발음 비교 & R/RR",
            "es": "Seseo LatAm vs. Distinción + R/RR",
        },
        "audios": [
            {
                "id": "es_split",
                "file": "es_split.mp3",
                "phrase": "¿Podemos pagar por separado?",
                "phonetic": "/poˈðemos paˈɣaɾ poɾ sepaˈ<b>ɾaðo</b>/ · por <b>separado</b>",
                "meaning": {
                    "en": "Can we pay separately?",
                    "zh-Hant": "請問我們可以分開結帳嗎？",
                    "zh-Hans": "请问我们可以分开结账吗？",
                    "ja": "別々にお支払いできますか？",
                    "ko": "따로 계산해도 될까요?",
                    "es": "Cómo pedir cuentas separadas en restaurante.",
                },
                "tag": {
                    "en": "Dining & Tapas · Split Bill",
                    "zh-Hant": "餐館分帳 · 日常必備",
                    "zh-Hans": "餐馆分账 · 日常必备",
                    "ja": "レストラン・別会計",
                    "ko": "식당 더치페이 · 필수 표현",
                    "es": "Restaurante · Cuenta separada",
                },
            },
            {
                "id": "es_card",
                "file": "es_card.mp3",
                "phrase": "¿Puedo pagar con tarjeta?",
                "phonetic": "/ˈpweðo paˈɣaɾ kon taɾˈ<b>x</b>eta/ · tar<b>j</b>eta (/x/)",
                "meaning": {
                    "en": "Can I pay by card?",
                    "zh-Hant": "請問我可以刷信用卡嗎？",
                    "zh-Hans": "请问我可以刷信用卡吗？",
                    "ja": "カードで支払えますか？",
                    "ko": "카드로 결제할 수 있나요?",
                    "es": "Preguntar pago con tarjeta en tienda.",
                },
                "tag": {
                    "en": "Checkout · Spanish Jota /x/",
                    "zh-Hant": "結帳刷卡 · 喉音 J /x/",
                    "zh-Hans": "结账刷卡 · 喉音 J /x/",
                    "ja": "会計・喉音 J /x/",
                    "ko": "카드 결제 · 후음 J /x/",
                    "es": "Caja · Sonido J /x/",
                },
            },
        ],
    },
    {
        "slug": "koreango",
        "name": "KoreanGo",
        "accent": "#2DD4BF",
        "accent_soft": "rgba(45, 212, 191, 0.16)",
        "flag": "🇰🇷",
        "app_store_id": "6838241626",
        "app_store_url": "https://apps.apple.com/app/id6838241626",
        "website_url": "https://koreango.appengine.fun",
        "version": "1.0.0",
        "title": {
            "en": "KoreanGo — Korean",
            "zh-Hant": "KoreanGo — 旅遊韓語",
            "zh-Hans": "KoreanGo — 旅游韩语",
            "ja": "KoreanGo — 旅行韓国語",
            "ko": "KoreanGo — 여행 한국어",
            "es": "KoreanGo — Coreano de Viaje",
        },
        "pill_label": {
            "en": "Korean · KoreanGo",
            "zh-Hant": "韓語 · KoreanGo",
            "zh-Hans": "韩语 · KoreanGo",
            "ja": "韓国語 · KoreanGo",
            "ko": "한국어 · KoreanGo",
            "es": "Coreano · KoreanGo",
        },
        "tagline": {
            "en": "40 Hangul Jamo with stroke canvas, 24 3-way minimal pairs, 100 Seoul travel videos & 693 studio MP3s.",
            "zh-Hant": "40 韓文字母筆順手寫、24 組平音／激音／緊音辨音、100 部首爾實境影片與 693 錄音。",
            "zh-Hans": "40 韩文字母笔顺手写、24 组平音／送气音／紧音辨音、100 部首尔实景视频与 693 录音。",
            "ja": "ハングル40文字筆順、平音/激音/濃音24組聞き分け、ソウル動画100本＆693音声。",
            "ko": "한글 자모 40자 필순 쓰기, 평음·격음·경음 24쌍 훈련, 서울 회화 영상 100편 & 693 오디오.",
            "es": "40 letras Hangul con trazos, 24 pares triples, 100 vídeos en Seúl y 693 audios nativos.",
        },
        "specs": {
            "en": ["40 Hangul Jamo + Stroke Canvas", "24 3-Way Pairs · 5 Sound Rules", "100 Seoul Videos · 693 MP3s", "15 Units · 160 SM-2 Cards"],
            "zh-Hant": ["40 韓文字母＋互動手寫畫板", "24 組三向辨音 · 5 大音變規則", "100 首爾影片 · 693 支錄音", "15 堂課 · 160 張單字卡"],
            "zh-Hans": ["40 韩文字母＋互动手写画板", "24 组三向辨音 · 5 大音变规则", "100 首尔视频 · 693 支录音", "15 节课 · 160 张词卡"],
            "ja": ["ハングル40文字＋手書きボード", "3系列24組聞き分け · 音変化5則", "ソウル動画100本 · 693音声", "全15課 · 160語SM-2カード"],
            "ko": ["한글 40자＋인터랙티브 필순", "평·격·경음 24쌍 · 음운 규칙 5개", "서울 영상 100편 · 오디오 693개", "15 유닛 · 160 SM-2 카드"],
            "es": ["40 Hangul Jamo + trazos", "24 pares triples · 5 reglas clave", "100 vídeos en Seúl · 693 MP3s", "15 unidades · 160 tarjetas SRS"],
        },
        "script_col": {
            "en": "40 Hangul Jamo + Canvas",
            "zh-Hant": "40 韓文字母＋筆順手寫",
            "zh-Hans": "40 韩文字母＋笔顺手写",
            "ja": "ハングル40文字＋手書き",
            "ko": "한글 40자모＋필순 쓰기",
            "es": "40 Hangul Jamo + trazos",
        },
        "highlight_col": {
            "en": "Plain/Aspirated/Tense (불/풀/뿔) & Batchim",
            "zh-Hant": "平激緊音 (불/풀/뿔) 與收尾音韻變化",
            "zh-Hans": "平送紧音 (불/풀/뿔) 与收尾音韵变化",
            "ja": "平音/激音/濃音 (불/풀/뿔)＆パッチム",
            "ko": "평음·격음·경음 (불/풀/뿔) & 받침",
            "es": "Contraste suave/aspirada/tensa + batchim",
        },
        "audios": [
            {
                "id": "ko_split",
                "file": "ko_split.mp3",
                "phrase": "두 명 따로 계산해도 돼요?",
                "phonetic": "Du myeong <b>ttaro</b> gyesanhaedo dwaeyo? · [t͈a.ɾo]",
                "meaning": {
                    "en": "Can the two of us pay separately?",
                    "zh-Hant": "請問兩個人分開結帳可以嗎？",
                    "zh-Hans": "请问两个人分开结账可以吗？",
                    "ja": "2人別々にお会計してもいいですか？",
                    "ko": "식당에서 두 명이 따로 계산할 때 쓰는 표현.",
                    "es": "¿Podemos pagar los dos por separado?",
                },
                "tag": {
                    "en": "Dining · Tense Consonant tt (따)",
                    "zh-Hant": "餐廳分帳 · 緊音 ㄸ (따로)",
                    "zh-Hans": "餐厅分账 · 紧音 ㄸ (따로)",
                    "ja": "レストラン · 濃音 ㄸ (따로)",
                    "ko": "식당 결제 · 경음 ㄸ (따로)",
                    "es": "Restaurante · Consonante tensa ㄸ",
                },
            },
            {
                "id": "ko_slowly",
                "file": "ko_slowly.mp3",
                "phrase": "조금만 천천히 말씀해 주세요.",
                "phonetic": "Jogeumman <b>cheoncheoni</b> malsseumhae juseyo.",
                "meaning": {
                    "en": "Please speak just a little more slowly.",
                    "zh-Hant": "麻煩請再說慢一點點。",
                    "zh-Hans": "麻烦请再说慢一点点。",
                    "ja": "もう少しゆっくり話してください。",
                    "ko": "상대방에게 조금 천천히 말해달라고 부탁하는 표현.",
                    "es": "Por favor, hable un poco más despacio.",
                },
                "tag": {
                    "en": "Polite Rescue · Soft Medial ㅎ",
                    "zh-Hant": "禮貌必備句 · 弱化音 ㅎ",
                    "zh-Hans": "礼貌救援句 · 弱化音 ㅎ",
                    "ja": "必須フレーズ · 弱音化 ㅎ",
                    "ko": "회화 필수 · ㅎ 약화 발음",
                    "es": "Frase clave · Debilitación ㅎ",
                },
            },
        ],
    },
    {
        "slug": "mandaringo",
        "name": "MandarinGo",
        "accent": "#F59E0B",
        "accent_soft": "rgba(245, 158, 11, 0.16)",
        "flag": "🇹🇼",
        "app_store_id": "6838245896",
        "app_store_url": "https://apps.apple.com/app/id6838245896",
        "website_url": "https://mandaringo.appengine.fun",
        "version": "1.0.0",
        "title": {
            "en": "MandarinGo — Mandarin",
            "zh-Hant": "MandarinGo — 華語雙軌",
            "zh-Hans": "MandarinGo — 汉语双轨",
            "ja": "MandarinGo — 台湾＆中国語",
            "ko": "MandarinGo — 대만·중국어",
            "es": "MandarinGo — Chino Mandarín",
        },
        "pill_label": {
            "en": "Mandarin · MandarinGo",
            "zh-Hant": "中文 · MandarinGo",
            "zh-Hans": "中文 · MandarinGo",
            "ja": "中国語 · MandarinGo",
            "ko": "중국어 · MandarinGo",
            "es": "Mandarín · MandarinGo",
        },
        "tagline": {
            "en": "Dual Traditional + Zhuyin (ㄅㄆㄇㄈ) & Simplified + Pinyin switcher, 100 videos, 1,478 studio MP3s.",
            "zh-Hant": "一鍵切換「繁體字＋注音符號 (ㄅㄆㄇㄈ)」與「簡體字＋漢語拼音」，100 部影片、1,478 錄音。",
            "zh-Hans": "一键切换“简体字＋汉语拼音”与“繁体字＋注音符号 (ㄅㄆㄇㄈ)”，100 部视频、1,478 录音。",
            "ja": "繁体字＋注音符号と簡体字＋ピンインを瞬時に切替。動画100本＆1,478音声収録。",
            "ko": "대만 번체·주음(ㄅㄆㄇㄈ) ⇄ 중국 간체·병음 원터치 전환, 회화 영상 100편 & 1,478 오디오.",
            "es": "Cambia entre Tradicional + Zhuyin y Simplificado + Pinyin al instante; 100 vídeos y 1,478 audios.",
        },
        "specs": {
            "en": ["37 Zhuyin & Pinyin + 24 Tone Pairs", "TW ⇄ CN Term & Accent Switch", "100 HD Videos · 1,478 Studio MP3s", "15 Units · 160 SM-2 Cards"],
            "zh-Hant": ["37 注音／拼音＋24 組聲調辨音", "台灣 ⇄ 大陸雙軌詞彙口音切換", "100 高清短片 · 1,478 支錄音", "15 堂課 · 160 張單字卡"],
            "zh-Hans": ["37 注音／拼音＋24 组声调辨音", "两岸词汇／口音一键对照切换", "100 高清短片 · 1,478 支录音", "15 节课 · 160 张词卡"],
            "ja": ["37注音＆ピンイン＋24組声調", "台湾⇄大陸 語彙＆発音ワンタッチ切替", "100本HD動画 · 1,478本音声", "全15課 · 160語SM-2カード"],
            "ko": ["37 주음/병음 + 24 성조/발음 쌍", "대만 ⇄ 중국 어휘·발음 전환", "100편 HD 영상 · 1,478 오디오", "15 유닛 · 160 SM-2 카드"],
            "es": ["37 Zhuyin y Pinyin + 24 pares tonos", "Modo Taiwán ⇄ China continental", "100 vídeos HD · 1,478 MP3s", "15 unidades · 160 tarjetas SRS"],
        },
        "script_col": {
            "en": "37 Zhuyin & Pinyin + Strokes",
            "zh-Hant": "37 注音與拼音＋筆順",
            "zh-Hans": "37 注音与拼音＋笔顺",
            "ja": "37注音・ピンイン＋筆順",
            "ko": "37 주음부호/병음＋필순",
            "es": "37 Zhuyin y Pinyin + trazos",
        },
        "highlight_col": {
            "en": "Dual Traditional/Zhuyin ⇄ Simplified/Pinyin",
            "zh-Hant": "台灣注音繁體 ⇄ 大陸拼音簡體雙軌",
            "zh-Hans": "台湾注音繁体 ⇄ 大陆拼音简体双轨",
            "ja": "繁体字注音 ⇄ 簡体字ピンイン切替",
            "ko": "번체 주음 ⇄ 간체 병음 듀얼 모드",
            "es": "Dual Tradicional/Zhuyin ⇄ Simplificado/Pinyin",
        },
        "audios": [
            {
                "id": "zh_boba_tw",
                "file": "zh_boba_tw.mp3",
                "phrase": "我的烏龍奶茶要半糖少冰，謝謝。",
                "phonetic": "Wǒ de wūlóng nǎichá yào <b>bàntáng shǎobīng</b>, xièxie.",
                "meaning": {
                    "en": "Half sugar and less ice for my oolong milk tea, please.",
                    "zh-Hant": "台灣手搖飲料店點單必備：半糖＋少冰。",
                    "zh-Hans": "茶饮店点单常用表达：半糖＋少冰。",
                    "ja": "ウーロンミルクティーを半糖・氷少なめでお願いします。",
                    "ko": "우롱 밀크티 당도 50%, 얼음 적게 주세요.",
                    "es": "Medio azúcar y menos hielo para mi té oolong con leche.",
                },
                "tag": {
                    "en": "Boba Shop · Taiwan Order",
                    "zh-Hant": "手搖飲店 · 甜度冰塊口音",
                    "zh-Hans": "茶饮点单 · 甜度冰块表达",
                    "ja": "タピオカ店 · 甘さ・氷オーダー",
                    "ko": "버블티 · 대만 당도/얼음 주문",
                    "es": "Té Boba · Azúcar y hielo",
                },
            },
            {
                "id": "zh_pay_tw",
                "file": "zh_pay_tw.mp3",
                "phrase": "請問這裡可以刷卡嗎？",
                "phonetic": "Qǐngwèn zhèlǐ <b>kěyǐ shuākǎ</b> ma? · [ʂwa˥.kʰa˨˩˦]",
                "meaning": {
                    "en": "Excuse me, can I pay by credit card here?",
                    "zh-Hant": "台灣腔示範：結帳刷卡＋第三聲連讀變調 (kéyǐ)。",
                    "zh-Hans": "台湾声调示范：结账刷卡＋三声变调 (kéyǐ)。",
                    "ja": "すみません、ここはクレジットカードを使えますか？",
                    "ko": "실례지만 여기 신용카드 결제되나요?",
                    "es": "Disculpe, ¿puedo pagar con tarjeta aquí?",
                },
                "tag": {
                    "en": "Checkout · 3rd Tone Sandhi",
                    "zh-Hant": "結帳刷卡 · 三聲連讀變調",
                    "zh-Hans": "结账刷卡 · 三声变调示范",
                    "ja": "会計 · 第3声の声調変化",
                    "ko": "결제 · 제3성 성조 변화",
                    "es": "Pago · Sandhi de 3er tono",
                },
            },
        ],
    },
]

COMPARISON_ITEMS = [
    {
        "slug": "nihongo",
        "app_name": "NihonGo",
        "lang_badge": "🇯🇵 日本語 · JP",
        "file": "jp_split.mp3",
        "phrase": "お会計は別々でお願いします。",
        "phonetic": "o kaikei <b>wa</b> betsubetsu de o negai shi masu",
        "meaning": {
            "en": "Separate checks, please.",
            "zh-Hant": "結帳麻煩分開算。",
            "zh-Hans": "结账麻烦分开算。",
            "ja": "別々にお会計をお願いする表現。",
            "ko": "계산은 따로 부탁드립니다.",
            "es": "La cuenta por separado, por favor.",
        },
    },
    {
        "slug": "englishgo",
        "app_name": "EnglishGo",
        "lang_badge": "🇺🇸 English · EN",
        "file": "en_card.mp3",
        "phrase": "Do you take credit cards or Apple Pay?",
        "phonetic": "/duː juː teɪk <b>ˈkrɛdɪt kɑːrdz</b> ɔːr ˈæpəl peɪ/",
        "meaning": {
            "en": "Asking about cards / Apple Pay.",
            "zh-Hant": "請問你們收信用卡或 Apple Pay 嗎？",
            "zh-Hans": "请问你们收信用卡或 Apple Pay 吗？",
            "ja": "クレジットカードかApple Payは使えますか？",
            "ko": "신용카드나 애플페이 결제 되나요?",
            "es": "¿Aceptan tarjetas de crédito o Apple Pay?",
        },
    },
    {
        "slug": "espanolgo",
        "app_name": "EspanolGo",
        "lang_badge": "🇪🇸 Español · ES",
        "file": "es_split.mp3",
        "phrase": "¿Podemos pagar por separado?",
        "phonetic": "/poˈðemos paˈɣaɾ poɾ sepaˈ<b>ɾaðo</b>/",
        "meaning": {
            "en": "Can we pay separately?",
            "zh-Hant": "請問我們可以分開結帳嗎？",
            "zh-Hans": "请问我们可以分开结账吗？",
            "ja": "別々にお支払いできますか？",
            "ko": "따로 계산해도 될까요?",
            "es": "Pedir cuentas separadas.",
        },
    },
    {
        "slug": "koreango",
        "app_name": "KoreanGo",
        "lang_badge": "🇰🇷 한국어 · KR",
        "file": "ko_split.mp3",
        "phrase": "두 명 따로 계산해도 돼요?",
        "phonetic": "Du myeong <b>ttaro</b> gyesanhaedo dwaeyo?",
        "meaning": {
            "en": "Can the two of us pay separately?",
            "zh-Hant": "請問兩個人分開結帳可以嗎？",
            "zh-Hans": "请问两个人分开结账可以吗？",
            "ja": "2人別々にお会計してもいいですか？",
            "ko": "두 명이 따로 계산하기.",
            "es": "¿Podemos pagar los dos por separado?",
        },
    },
    {
        "slug": "mandaringo",
        "app_name": "MandarinGo (TW)",
        "lang_badge": "🇹🇼 台灣華語 · TW",
        "file": "zh_pay_tw.mp3",
        "phrase": "請問這裡可以刷卡嗎？",
        "phonetic": "ㄑㄧㄥˇ ㄨㄣˋ ㄓㄜˋ ㄌㄧˇ ㄎㄜˇ ㄧˇ ㄕㄨㄚ ㄎㄚˇ ㄇㄚ˙？",
        "meaning": {
            "en": "Excuse me, can I pay by card? (Taiwan)",
            "zh-Hant": "台灣腔示範：請問這裡可以刷卡嗎？",
            "zh-Hans": "台湾口音：请问这里可以刷卡吗？",
            "ja": "すみません、カードを使えますか？（台湾）",
            "ko": "여기 카드 결제되나요? (대만 억양)",
            "es": "¿Puedo pagar con tarjeta? (Taiwán)",
        },
    },
    {
        "slug": "mandaringo",
        "app_name": "MandarinGo (CN)",
        "lang_badge": "🇨🇳 普通话 · CN",
        "file": "zh_pay_cn.mp3",
        "phrase": "请问这里可以刷卡吗？",
        "phonetic": "Qǐngwèn zhèlǐ <b>kěyǐ shuākǎ</b> ma?",
        "meaning": {
            "en": "Excuse me, can I pay by card? (Mainland)",
            "zh-Hant": "大陸普通話示範：請問這裡可以刷卡嗎？",
            "zh-Hans": "普通话示范：请问这里可以刷卡吗？",
            "ja": "すみません、カードを使えますか？（中国本土）",
            "ko": "여기 카드 결제되나요? (중국 본토)",
            "es": "¿Puedo pagar con tarjeta? (China)",
        },
    },
]

CONTENT = {
    "en": {
        "html_lang": "en",
        "title": "AE Languages — 5 Native Travel Language Apps for iPhone & iPad",
        "desc": "Explore all 5 AE Interactive Travel Language Go apps—NihonGo, EnglishGo, EspanolGo, KoreanGo, and MandarinGo. 500 real travel dialogue videos, interactive sound labs, guided voice practice, live 2-way translation, and zero tracking.",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,travel language apps,Japanese,Korean,Spanish,English,Mandarin,iOS",
        "brand_name": "AE Languages",
        "nav_apps": "5 Apps",
        "nav_compare": "Audio Compare",
        "nav_matrix": "Matrix",
        "nav_privacy": "Privacy",
        "nav_support": "Support",
        "nav_studio": "AE Studio",
        "hero_badge": "5 LIVE APPS · IPHONE, IPAD & IPHONE DUO · ZERO ACCOUNTS · ZERO ADS",
        "hero_title": "Speak Real Travel Phrases Across <span>5 Languages</span>",
        "hero_sub": "Japanese, English, Spanish, Korean, and Mandarin—each built natively in Swift with 15 structured lessons, 100 real-world travel dialogue videos, interactive sound labs, 12-scene Guided Voice Practice, and live 2-way translation.",
        "status_pill": "All 5 Apps Live Now on App Store · Free Forever + Optional $3.99 Lifetime Pro",
        "cta_primary": "Choose Your Language ↓",
        "cta_audio": "▶ Compare 5 Languages",
        "cta_matrix": "See Full Suite ↓",
        "stat_items": [
            ("5", "Target Languages"),
            ("500", "Real Travel Videos"),
            ("3,000+", "Studio MP3 Clips"),
            ("60", "Voice Roleplay Scenes"),
            ("$0 / $3.99", "Free Tier + One-Time Pro"),
        ],
        "picker_badge": "WHERE ARE YOU FLYING NEXT?",
        "picker_title": "Pick a Destination to Preview Inside the App",
        "picker_sub": "Tap any language below to hear actual bundled studio MP3s, inspect real iPhone previews, and jump straight to App Store or its dedicated site.",
        "btn_appstore_sub": "Download Free on",
        "btn_appstore_main": "App Store",
        "btn_site": "Open Official Site →",
        "btn_play": "Play",
        "btn_playing": "Playing",
        "btn_focus": "Inspect ↑",
        "cmp_badge": "SAME MOMENT · FIVE LANGUAGES",
        "cmp_title": "Hear Checkout Phrases Side-by-Side",
        "cmp_sub": "Every phrase below plays directly from the real studio audio bundled inside NihonGo, EnglishGo, EspanolGo, KoreanGo, and MandarinGo.",
        "grid_badge": "COMPLETE TRAVEL GO SUITE",
        "grid_title": "All 5 Native iOS & iPadOS Language Apps",
        "grid_sub": "Start free with full sound charts, 24 minimal pairs, 160 SM-2 flashcards, Units 1–3, 10 videos, and daily speaking turns—or unlock everything forever for $3.99.",
        "matrix_badge": "SIDE-BY-SIDE COMPARISON",
        "matrix_title": "Shared Architecture. Deep Language Craft.",
        "matrix_cols": ["App", "Target", "Script & Sound Lab", "Regional & Phonetic Craft", "Videos · Voice · Cards", "Price"],
        "matrix_common": "15 Units · 100 Videos · 12 Scenes · 160 Cards · Live 2-Way",
        "matrix_price": "Free · $3.99 Pro",
        "pillars_badge": "SHARED AE INTERACTIVE ARCHITECTURE",
        "pillars_title": "Built One Way Across All Five Languages",
        "pillars": [
            ("🎬", "100 Real Travel Video Dialogues Each", "500 chronological airport, café, dining, transit, hotel, and pharmacy video scenarios—200 studio audio recordings per app."),
            ("💬", "12 Guided Voice Roleplay Missions", "Local staff open the dialogue on-device while helpful native-script phrase hints stay visible onscreen as you respond."),
            ("🗣️", "Live 2-Way Voice Interpreter", "Speak or type between your native language and Japanese, English, Spanish, Korean, or Mandarin with fullscreen counter cards."),
            ("🔒", "Zero Sign-In · Zero Trackers", "No accounts, no ads, no third-party telemetry SDKs. Learning streaks and SRS flashcards stay locally inside Apple UserDefaults."),
        ],
        "privacy_title": "Privacy Policy — AE Travel Language Series",
        "privacy_updated": "Last Updated: November 26, 2026",
        "privacy_sections": [
            ("1. Zero Trackers Across This Hub & All 5 Apps", "languages.appengine.fun is operated by AE Interactive (AppEngine Interactive). This portal sets zero tracking cookies, includes zero analytics or advertising scripts, and shares strict zero-collection privacy with NihonGo, EnglishGo, EspanolGo, KoreanGo, and MandarinGo (App Store Privacy Nutrition Label: Data Not Collected / NSPrivacyTracking = false)."),
            ("2. On-Device Learning Progress & Apple Frameworks", "All flashcards, stroke tracing progress, preferences, and streaks are stored locally on your iPhone or iPad via Apple UserDefaults (Required Reason API CA92.1). Voice practice and live two-way translations run through Apple's native Speech, Translation, and system language frameworks without account sign-in."),
            ("3. Dedicated Privacy Policy Links per App", "You can also inspect app-specific privacy statements on nihongo.appengine.fun/privacy, englishgo.appengine.fun/privacy, espanolgo.appengine.fun/privacy, koreango.appengine.fun/privacy, and mandaringo.appengine.fun/privacy."),
            ("4. Contact AE Interactive", "Questions or privacy requests? Email help@appengine.fun."),
        ],
        "support_title": "Support & Compatibility — AE Travel Language Series",
        "support_sub": "System requirements, offline translation packs, App Store links, and direct developer support across all 5 apps.",
        "support_cards": [
            ("Offline Curriculum, Videos & Flashcards", "Every unit, 100 scenario videos, sound charts, handwriting canvas, 160 SM-2 flashcards, and 18 grammar drills work offline on any iPhone or iPad running iOS / iPadOS 17.0+ without creating an account."),
            ("Guided Voice Practice & Live 2-Way Translation", "On-device Guided Roleplay runs via Apple's native system language model on iOS / iPadOS 26.0+ (with full phrase-guided fallback on iOS 17+). Before flying, download offline Apple Translate language packs in iOS Settings -> Apps -> Translate."),
            ("One-Time $3.99 Lifetime Unlock + Restore", "Each app includes a generous Free Forever tier plus an optional $3.99 one-time Lifetime Pro upgrade (no subscriptions). Tap Restore Purchases on any device signed into your Apple ID."),
            ("Direct Support & App Pages", "Email AE Interactive at help@appengine.fun (typically replies within 24 hours), or visit each app's dedicated site below for FAQs."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "title": "AE Languages — 五大獨立語言旅遊學習 App 家族｜iPhone 與 iPad 原生打造",
        "desc": "一次瀏覽 AE Interactive 旗下 5 款原生語言旅遊 App：NihonGo（日語）、EnglishGo（英語）、EspanolGo（西語）、KoreanGo（韓語）與 MandarinGo（華語雙軌）。收錄 500 部實境對話影片、語音引導口說與雙向即時翻譯，免登入零追蹤。",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,語言學習App,旅遊日語,旅遊英語,旅遊西語,旅遊韓語,華語學習",
        "brand_name": "AE Languages",
        "nav_apps": "五大語言 App",
        "nav_compare": "五語聽比",
        "nav_matrix": "規格比較",
        "nav_privacy": "隱私權",
        "nav_support": "支援",
        "nav_studio": "AE 工作室",
        "hero_badge": "5 款 APP 全部上架 · 支援 IPHONE / IPAD / IPHONE DUO · 免登入零廣告",
        "hero_title": "一次掌握五大目的地的 <span>地道旅遊會話</span>",
        "hero_sub": "日語、英語、西語、韓語與華語雙軌——每款皆以 Swift 原生打造，整合 15 堂系統課、100 部實境對話短片、音標手寫與辨音挑戰、12 情境店員開口練習，以及現場雙向即時語音口譯。",
        "status_pill": "5 款 App 皆已在 App Store 正式上架 · 基礎永久免費 · 可選 $3.99 一次買斷 Pro",
        "cta_primary": "選擇目的地語言 ↓",
        "cta_audio": "▶ 五語同場試聽",
        "cta_matrix": "查看完整家族 ↓",
        "stat_items": [
            ("5", "目標學習語言"),
            ("500", "首爾/東京等實境短片"),
            ("3,000+", "錄音室真人 MP3"),
            ("60", "情境語音口說關卡"),
            ("$0 / $3.99", "免費暢學 + 單次買斷"),
        ],
        "picker_badge": "下一趟想飛去哪裡？",
        "picker_title": "點選語言，搶先體驗各 App 真實語音與畫面",
        "picker_sub": "切換下方五大語言標籤，直接播放 App 內收錄的原生錄音、預覽實機介面並前往 App Store 免費下載。",
        "btn_appstore_sub": "立即前往下載",
        "btn_appstore_main": "App Store",
        "btn_site": "前往專屬官網 →",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "btn_focus": "上方詳情 ↑",
        "cmp_badge": "同一旅遊情境 · 五國語言同台發聲",
        "cmp_title": "點一下，聽五國結帳與分帳真實語音",
        "cmp_sub": "以下音檔皆擷取自 NihonGo、EnglishGo、EspanolGo、KoreanGo 與 MandarinGo（含台灣與大陸雙口音）真實上架內容。",
        "grid_badge": "AE TRAVEL GO 完整產品陣容",
        "grid_title": "五款獨立開發、零訂閱壓力的原生語言 App",
        "grid_sub": "每款皆可永久免費學完完整字音表、24 組辨音挑戰、160 張單字卡、前 3 堂課與 10 部實境短片；需要全部內容隨時以 $3.99 一次永久買斷。",
        "matrix_badge": "全系列能力一覽",
        "matrix_title": "一致的極簡體驗・針對各語言量身打磨",
        "matrix_cols": ["App 名稱", "目標語言", "書寫與音標實驗室", "獨家在地發音亮點", "影片 · 口說 · 詞卡", "價格方案"],
        "matrix_common": "15 課 · 100 影片 · 12 情境 · 160 詞卡 · 雙向口譯",
        "matrix_price": "免費 · $3.99 買斷",
        "pillars_badge": "五大核心共同標準",
        "pillars_title": "每一款都為真實機場、餐廳與地鐵現場而生",
        "pillars": [
            ("🎬", "每款標配 100 部實境旅遊對話短片", "全系列共 500 支場景影片涵蓋點餐、買美妝退稅、地鐵轉乘、飯店與就醫，每款附 200 句真人錄音與羅馬／IPA 音標。"),
            ("💬", "12 情境店員主動開場口說練習", "由當地店員先開口提問，錄音回答時畫面保留關鍵字詞提示，幫你克服不敢開口的緊張感。"),
            ("🗣️", "底部一鍵直達雙向即時口譯", "支援語音與鍵盤雙向即時互譯與大字全螢幕字卡，沒網路也能搭配離線翻譯包即時溝通。"),
            ("🔒", "免註冊登入・零廣告零追蹤", "不含任何廣告聯播網與第三方分析 SDK，學習進度與複習紀錄僅保存於您的本機 UserDefaults。"),
        ],
        "privacy_title": "隱私權政策 — AE Languages 語言系列總站",
        "privacy_updated": "最後更新日期：2026 年 11 月 26 日",
        "privacy_sections": [
            ("1. 總站與五大 App 一致維持零追蹤承諾", "languages.appengine.fun 由 AE Interactive 維運。本網站不設置追蹤 Cookie、不載入廣告與第三方分析腳本，並與 NihonGo、EnglishGo、EspanolGo、KoreanGo、MandarinGo 同樣遵守「不收集任何資料」（NSPrivacyTracking = false）。"),
            ("2. 裝置本機進度儲存與 Apple 原生架構", "五款 App 的字音學習紀錄、SRS 複習進度與字級偏好皆透過標準 Apple UserDefaults（CA92.1）存於設備本機端，語音口說與翻譯優先調用 Apple 原生框架，無需註冊帳號。"),
            ("3. 各款 App 專屬隱私權頁面", "您亦可隨時檢閱 nihongo.appengine.fun/privacy、englishgo.appengine.fun/privacy、espanolgo.appengine.fun/privacy、koreango.appengine.fun/privacy 與 mandaringo.appengine.fun/privacy。"),
            ("4. 聯絡 AE Interactive", "任何疑問請來信 help@appengine.fun。"),
        ],
        "support_title": "技術支援與相容說明 — AE Languages 總站",
        "support_sub": "系統需求、離線翻譯包教學與五大語言 App 客服入口。",
        "support_cards": [
            ("離線課程、實境影片與單字卡支援機型", "五款 App 內的所有 15 堂課、100 部影片、發音表、筆順畫板、160 張單字卡與 18 堂文法皆支援 iOS / iPadOS 17.0 以上機型離線使用，完全免登入。"),
            ("語音情境模擬與離線雙向翻譯包設定", "裝置端語音系統語言架構適用於 iOS / iPadOS 26.0+ 支援機型（所有 iOS 17+ 機型皆具備文字與關鍵句引導練習）。建議行前至系統「設定 → App → 翻譯」預載離線語言包。"),
            ("$3.99 一次永久買斷與恢復購買", "各款 App 皆提供完整永久免費基礎版，並可選擇 $3.99 單次永久解鎖 Pro（絕無自動訂閱扣款），換機可點擊「恢復購買」免額外付費。"),
            ("客服聯繫窗口", "有任何建議或需要協助請寄信至 help@appengine.fun（通常 24 小時內回覆），或點選下方各 App 官網檢視詳細 FAQ。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有權利。",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "title": "AE Languages — 五大独立语言旅游学习 App 家族｜iPhone & iPad 原生打造",
        "desc": "集中了解 AE Interactive 旗下 5 款原生语言旅游 App：NihonGo（日语）、EnglishGo（英语）、EspanolGo（西语）、KoreanGo（韩语）与 MandarinGo（汉语双轨）。500 个实景对话视频、语音引导口语及双向翻译，免登录零追踪。",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,语言学习App,旅游日语,旅游英语,旅游西语,旅游韩语,汉语学习",
        "brand_name": "AE Languages",
        "nav_apps": "五大语言 App",
        "nav_compare": "五语试听",
        "nav_matrix": "规格对比",
        "nav_privacy": "隐私政策",
        "nav_support": "技术支持",
        "nav_studio": "AE 工作室",
        "hero_badge": "5 款 APP 全部上线 · 支持 IPHONE / IPAD / IPHONE DUO · 免登录零广告",
        "hero_title": "轻松拿下五大旅行目的地的 <span>地道当地会话</span>",
        "hero_sub": "日语、英语、西语、韩语与汉语双轨——每款均采用纯 Swift 原生打造，整合 15 节系统课程、100 个实景对话视频、音标描红与辨音特训、12 情景店员开口模拟及现场双向实时翻译。",
        "status_pill": "5 款 App 均已在 App Store 正式上线 · 基础永久免费 · 可选 $3.99 一次买断 Pro",
        "cta_primary": "选择目的地语言 ↓",
        "cta_audio": "▶ 五语同场对比",
        "cta_matrix": "查看完整家族 ↓",
        "stat_items": [
            ("5", "目标学习语言"),
            ("500", "实景旅游视频场景"),
            ("3,000+", "录音室真人 MP3"),
            ("60", "互动开口情景关卡"),
            ("$0 / $3.99", "免费学基础 + 单次买断"),
        ],
        "picker_badge": "下一站飞去哪里？",
        "picker_title": "点击下方语言，抢先试听各 App 真人发音与界面",
        "picker_sub": "切换五大语言胶囊卡片，直接试听内置高清录音、查看实机截图并直达 App Store 免费下载。",
        "btn_appstore_sub": "前往免费下载",
        "btn_appstore_main": "App Store",
        "btn_site": "访问专属官网 →",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "btn_focus": "顶部详情 ↑",
        "cmp_badge": "同一出行场景 · 五国语言同屏听对比",
        "cmp_title": "点击对比五国语言地道结账与刷卡说法",
        "cmp_sub": "以下音频直接采自 NihonGo、EnglishGo、EspanolGo、KoreanGo 及 MandarinGo（含台湾与普通话双口音）正式上架版本。",
        "grid_badge": "AE TRAVEL GO 全系矩阵",
        "grid_title": "五款原生无广告、拒绝订阅制的旅游语言 App",
        "grid_sub": "每款均可免费学完完整音表、24 组辨音挑战、160 张词卡、前 3 节课程与 10 支实景短片；满意后可一次 $3.99 永久解锁全套。",
        "matrix_badge": "全系列横向对比",
        "matrix_title": "统一极简架构 · 针对每种语言深度打磨",
        "matrix_cols": ["App 名称", "目标语言", "文字与语音实验室", "专属发音教学特色", "视频 · 口语 · 词卡", "价格方案"],
        "matrix_common": "15 课 · 100 视频 · 12 情景 · 160 词卡 · 双向口译",
        "matrix_price": "免费 · $3.99 买断",
        "pillars_badge": "全系共享四大产品坚持",
        "pillars_title": "专为机场通关、点餐点饮与地铁换乘而生",
        "pillars": [
            ("🎬", "每款均附 100 个实景对话短视频", "全系共 500 个实拍旅游情境视频，附带 200 句原生真人录音、音标 IPA 与实用出行礼仪小贴士。"),
            ("💬", "12 情景由店员先开口的互动模拟", "店员先提问、录音时画面持续显示关键提示句，助你跨出开口说外语的第一步。"),
            ("🗣️", "底栏一键直达双向实时翻译", "支持语音与键盘双输入，带全屏大字卡片给本地店员看，出行前下载离线包无网也能译。"),
            ("🔒", "免账号登录 · 零广告零追踪", "绝不接入任何广告或第三方统计 SDK，学习进度仅保存于您的设备本地 UserDefaults。"),
        ],
        "privacy_title": "隐私政策 — AE Languages 语言家族门户",
        "privacy_updated": "最后更新日期：2026 年 11 月 26 日",
        "privacy_sections": [
            ("1. 门户站与五款 App 统一坚持零追踪", "languages.appengine.fun 由 AE Interactive 运营。本网站不设追踪 Cookie，不加载广告或统计脚本，与旗下五款应用同样遵守 App Store“不收集数据”声明（NSPrivacyTracking = false）。"),
            ("2. 本地存储与端侧框架", "五款应用的学习记录与词卡间隔仅保存于本地 Apple UserDefaults（CA92.1），语音口语及双向翻译优先调用 Apple 原生框架运行，免注册登录。"),
            ("3. 各款 App 独立隐私页面", "您可分别访问 nihongo.appengine.fun/privacy、englishgo.appengine.fun/privacy、espanolgo.appengine.fun/privacy、koreango.appengine.fun/privacy 与 mandaringo.appengine.fun/privacy。"),
            ("4. 联系我们", "如有隐私疑问，请发送邮件至 help@appengine.fun。"),
        ],
        "support_title": "技术支持与常见问题 — AE Languages",
        "support_sub": "设备系统要求、离线翻译包预载指引与开发者支持。",
        "support_cards": [
            ("离线课程、视频与词卡兼容范围", "所有 15 节课程、100 个实景视频、发音表、手写画板、160 张记忆卡与 18 节语法测验在 iOS / iPadOS 17.0 及以上设备免登录离线可用。"),
            ("互动语音练习与离线翻译包配置", "端侧系统语言对话支持 iOS / iPadOS 26.0+ 兼容机型，全系 iOS 17+ 均保留关键短语引导。出行前可在“系统设置 → App → 翻译”下载离线包。"),
            ("$3.99 永久买断与恢复购买", "每款均提供大方永久免费版及 $3.99 单次买断 Pro，无任何订阅自动续费；更换设备点击“恢复购买”即可同步。"),
            ("联系支持团队", "如遇问题请写信至 help@appengine.fun（通常 24 小时内回复），或前往各 App 独立网站查看详情。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有权利。",
    },
    "ja": {
        "html_lang": "ja",
        "title": "AE Languages — 5言語トラベル語学アプリ公式ポータル｜iPhone & iPad",
        "desc": "AE Interactive のトラベル語学シリーズ全5アプリ（NihonGo・EnglishGo・EspanolGo・KoreanGo・MandarinGo）を一括紹介。計500本の現地会話動画、音声練習、双方向音声通訳をアカウント不要・広告ゼロで。",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,語学学習アプリ,英語,韓国語,スペイン語,中国語,日本語",
        "brand_name": "AE Languages",
        "nav_apps": "5つのアプリ",
        "nav_compare": "5言語聴き比べ",
        "nav_matrix": "機能比較",
        "nav_privacy": "プライバシー",
        "nav_support": "サポート",
        "nav_studio": "AE スタジオ",
        "hero_badge": "全5アプリ配信中 · IPHONE / IPAD / IPHONE DUO 対応 · アカウント不要",
        "hero_title": "旅先のリアルな一言を、<span>5つの言語でそのまま口に</span>",
        "hero_sub": "日本語・英語・スペイン語・韓国語・中国語。すべて Swift ネイティブ製で、15課カリキュラム・現地実境会話動画100本・発音＆筆順ラボ・12場面ロールプレイ・リアルタイム双方向通訳を搭載。",
        "status_pill": "全5アプリ App Store 配信中 · ずっと無料スタート · Pro 一度きり $3.99",
        "cta_primary": "言語を選ぶ ↓",
        "cta_audio": "▶ 5言語を聴き比べる",
        "cta_matrix": "全アプリ一覧 ↓",
        "stat_items": [
            ("5", "対応ターゲット言語"),
            ("500", "実境トラベル動画"),
            ("3,000+", "スタジオ収録音声"),
            ("60", "実践音声ロールプレイ"),
            ("$0 / $3.99", "無料枠 + 買い切りPro"),
        ],
        "picker_badge": "次の目的地はどこですか？",
        "picker_title": "言語を選んで各アプリの音声と画面をプレビュー",
        "picker_sub": "下のタブを切り替えると、各アプリに収録されている本物のMP3音声・実機画面・App Storeリンクをすぐに確認できます。",
        "btn_appstore_sub": "App Store で入手",
        "btn_appstore_main": "App Store",
        "btn_site": "公式サイトを見る →",
        "btn_play": "再生",
        "btn_playing": "再生中",
        "btn_focus": "上へ ↑",
        "cmp_badge": "同じ旅のシーン · 5言語サウンド比較",
        "cmp_title": "お会計・カード払いのフレーズを5言語で聴き比べ",
        "cmp_sub": "NihonGo・EnglishGo・EspanolGo・KoreanGo・MandarinGo（台湾＆中国本土の両発音）に収録されたネイティブ音声をワンタップ再生。",
        "grid_badge": "TRAVEL LANGUAGE GO ファミリー",
        "grid_title": "サブスクなし・広告なし・全5アプリ完全ラインナップ",
        "grid_sub": "全アプリ、発音チャート・聞き分け24組・160単語帳・1〜3課・動画10本がずっと無料。気に入ったら $3.99 一度きりの買い切りで全解放できます。",
        "matrix_badge": "スペック一覧",
        "matrix_title": "統一された使いやすさ。言語ごとの深いこだわり。",
        "matrix_cols": ["アプリ", "学習言語", "文字＆発音ラボ", "言語別の独自特徴", "動画 · 会話 · 単語帳", "価格"],
        "matrix_common": "15課 · 動画100本 · 12場面 · 160語 · 双方向通訳",
        "matrix_price": "無料 · $3.99 Pro",
        "pillars_badge": "全5アプリ共通の設計思想",
        "pillars_title": "空港・カフェ・地下鉄でそのまま使える実戦設計",
        "pillars": [
            ("🎬", "各アプリに現地実境動画 100本（合計500本）", "空港、カフェ、飲食、ショッピング、地下鉄乗り換え、緊急時まで旅の動線に沿って収録（各200音声）。"),
            ("💬", "店員から話しかける12場面ロールプレイ", "現地スタッフの質問からスタートし、画面上のヒントを見ながら声に出して3ステップの会話練習。"),
            ("🗣️", "右端タブから即起動・双方向音声通訳", "自国語 ⇄ 現地語を音声とテキストで即時翻訳。店員に見せられる全画面カード付きでオフライン翻訳パックにも対応。"),
            ("🔒", "ログイン不要・トラッキングゼロ", "広告SDKや外部アナリティクスは一切なし。学習履歴は端末内の Apple UserDefaults にのみ保存されます。"),
        ],
        "privacy_title": "プライバシーポリシー — AE Languages",
        "privacy_updated": "最終更新日：2026年11月26日",
        "privacy_sections": [
            ("1. 当ポータルおよび全5アプリのゼロ・トラッキング方針", "languages.appengine.fun は AE Interactive が運営しています。追跡Cookie、広告、アナリティクスを一切含まず、全5アプリと同様に App Store「データ収集なし」（NSPrivacyTracking = false）を徹底しています。"),
            ("2. オンデバイス処理と端末内データ保存", "単語帳・筆順の進捗・文字サイズ設定はすべて端末内の Apple UserDefaults（CA92.1）に保存され、音声練習および双方向翻訳は Apple 純正フレームワークにより端末上を優先して動作します。"),
            ("3. 各アプリの個別プライバシーページ", "nihongo.appengine.fun/privacy、englishgo.appengine.fun/privacy、espanolgo.appengine.fun/privacy、koreango.appengine.fun/privacy、mandaringo.appengine.fun/privacy もご確認いただけます。"),
            ("4. お問い合わせ", "ご質問は help@appengine.fun までお送りください。"),
        ],
        "support_title": "サポート＆動作環境 — AE Languages",
        "support_sub": "5アプリ共通の対応iOS要件、オフライン翻訳パックの設定方法、および窓口のご案内。",
        "support_cards": [
            ("オフライン学習コンテンツの動作環境", "全15課、実境動画100本、発音ラボ、手書きボード、160単語帳、文法18問はすべてアカウント登録なしで iOS / iPadOS 17.0 以降の iPhone・iPad でオフライン動作します。"),
            ("音声ロールプレイとオフライン翻訳パック設定", "オンデバイス音声システム言語モデルは iOS / iPadOS 26.0+ 対応機種でフル動作し、すべての iOS 17+ 端末でフレーズガイドが利用可能です。旅行前に「設定 → アプリ → 翻訳」から言語パックをダウンロードしてください。"),
            ("$3.99 買い切り Pro と購入の復元", "全アプリに永続無料枠と一度きり $3.99 の買い切り Pro（月額課金なし）を用意。機種変更時は「購入を復元」で即時復元できます。"),
            ("開発者サポート窓口", "ご不明点は help@appengine.fun まで（通常24時間以内にご返信）。各アプリの詳細は下記の個別サイトでもご確認いただけます。"),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
    },
    "ko": {
        "html_lang": "ko",
        "title": "AE Languages — 여행 외국어 앱 5종 포털｜iPhone & iPad 네이티브",
        "desc": "AE Interactive의 5가지 네이티브 여행 외국어 앱(NihonGo, EnglishGo, EspanolGo, KoreanGo, MandarinGo)을 한눈에 살펴보세요. 총 500편 실전 회화 영상, 발음·필기 연구실, 12장면 말하기 연습 및 양방향 실시간 통역.",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,여행 일본어,여행 영어,여행 스페인어,여행 한국어,중국어 앱",
        "brand_name": "AE Languages",
        "nav_apps": "앱 5종",
        "nav_compare": "음성 비교",
        "nav_matrix": "비교표",
        "nav_privacy": "개인정보",
        "nav_support": "고객지원",
        "nav_studio": "AE 스튜디오",
        "hero_badge": "5개 앱 정식 출시 · IPHONE / IPAD / IPHONE DUO 지원 · 로그인/광고 없음",
        "hero_title": "다음 여행지에서 바로 통하는 <span>5개 언어 실전 회화</span>",
        "hero_sub": "일본어·영어·스페인어·한국어·중국어를 각각 100% 네이티브 Swift로 제작했습니다. 15개 핵심 유닛, 실전 여행 회화 영상 100편, 발음·필기 랩, 12장면 음성 롤플레이, 양방향 실시간 통역을 무료로 시작하세요.",
        "status_pill": "App Store 5개 앱 전체 정식 출시 · 무료 기본 제공 · 평생 잠금해제 $3.99",
        "cta_primary": "언어 선택하기 ↓",
        "cta_audio": "▶ 5개국어 음성 비교",
        "cta_matrix": "전체 라인업 보기 ↓",
        "stat_items": [
            ("5", "지원 학습 언어"),
            ("500", "현지 실전 회화 영상"),
            ("3,000+", "스튜디오 원어민 MP3"),
            ("60", "실전 말하기 미션"),
            ("$0 / $3.99", "무료 시작 + 1회 평생 구매"),
        ],
        "picker_badge": "다음 여행지는 어디인가요?",
        "picker_title": "원하는 언어를 눌러 오디오와 실제 화면을 미리 보세요",
        "picker_sub": "아래 5가지 언어 탭을 클릭하면 각 앱에 수록된 실제 원어민 음성, 스크린샷, App Store 다운로드 및 공식 사이트로 바로 이동할 수 있습니다.",
        "btn_appstore_sub": "무료 다운로드",
        "btn_appstore_main": "App Store",
        "btn_site": "공식 사이트 열기 →",
        "btn_play": "재생",
        "btn_playing": "재생 중",
        "btn_focus": "상세 보기 ↑",
        "cmp_badge": "같은 여행 순간 · 5개 언어 원어민 비교",
        "cmp_title": "계산·카드 결제 표현을 5개 언어로 바로 비교해 보세요",
        "cmp_sub": "NihonGo, EnglishGo, EspanolGo, KoreanGo, MandarinGo(대만·중국 본토 성조 포함)에 실제로 내장된 스튜디오 오디오입니다.",
        "grid_badge": "AE TRAVEL GO 시리즈 전체 보기",
        "grid_title": "구독 결제·광고 없는 5가지 네이티브 외국어 앱",
        "grid_sub": "모든 앱은 음운 차트, 24쌍 듣기 훈련, 160 SM-2 단어 카드, 레슨 1~3 및 영상 10편을 영구 무료로 제공하며 $3.99 1회 결제로 전체를 잠금 해제할 수 있습니다.",
        "matrix_badge": "한눈에 보는 비교표",
        "matrix_title": "하나의 직관적인 학습 흐름, 언어별 맞춤 설계",
        "matrix_cols": ["앱 이름", "학습 언어", "문자 · 음운 연구실", "언어별 핵심 특화 기능", "영상 · 회화 · 카드", "가격"],
        "matrix_common": "15유닛 · 영상 100편 · 12장면 · 160카드 · 양방향 통역",
        "matrix_price": "무료 · $3.99 Pro",
        "pillars_badge": "5개 앱 공통 철학",
        "pillars_title": "공항·카페·지하철에서 한 손으로 바로 쓰는 실용성",
        "pillars": [
            ("🎬", "앱당 100편, 총 500편의 현지 회화 영상", "공항, 카페, 식당, 쇼핑, 지하철 환승, 응급 상황까지 실제 동선에 맞춰 구성(앱당 원어민 오디오 200개)."),
            ("💬", "직원이 먼저 말을 거는 12장면 말하기 연습", "상대방 질문으로 대화가 시작되며 화면 위 한국어·원어 힌트 카드를 보며 자연스럽게 3단계를 완주합니다."),
            ("🗣️", "오른쪽 탭 원터치 양방향 실시간 통역", "음성·키보드 양방향 번역과 직원에게 바로 보여주는 전체 화면 큰 글씨 카드를 지원합니다."),
            ("🔒", "계정 가입 없음 · 광고/추적 제로", "광고 SDK 및 외부 추적 코드가 전혀 없으며 학습 기록은 Apple UserDefaults로 기기에만 안전하게 저장됩니다."),
        ],
        "privacy_title": "개인정보 처리방침 — AE Languages",
        "privacy_updated": "최종 업데이트: 2026년 11월 26일",
        "privacy_sections": [
            ("1. 포털 및 5개 앱 전체 추적 제로 원칙", "languages.appengine.fun은 AE Interactive가 운영하며 추적 쿠키, 광고, 서드파티 분석 스크립트를 사용하지 않습니다. 모든 5개 앱은 App Store '수집되는 데이터 없음'(NSPrivacyTracking = false)을 준수합니다."),
            ("2. 기기 내 저장 및 Apple 네이티브 처리", "단어 카드 복습, 필기 진도, 글꼴 크기 설정은 기기 내부 Apple UserDefaults(CA92.1)에만 저장되며 음성 연습 및 양방향 번역은 Apple 네이티브 프레임워크를 통해 실행됩니다."),
            ("3. 각 앱별 개인정보 안내 페이지", "nihongo.appengine.fun/privacy, englishgo.appengine.fun/privacy, espanolgo.appengine.fun/privacy, koreango.appengine.fun/privacy, mandaringo.appengine.fun/privacy에서도 확인할 수 있습니다."),
            ("4. 문의처", "개인정보 및 앱 관련 문의는 help@appengine.fun으로 보내주세요."),
        ],
        "support_title": "고객지원 및 호환 안내 — AE Languages",
        "support_sub": "5개 앱 공통 iOS 호환성, 오프라인 번역 팩 설치 안내 및 개발자 지원 채널.",
        "support_cards": [
            ("오프라인 학습·영상·단어장 지원 기기", "모든 15개 유닛, 100편 영상, 발음 차트, 필순 캔버스, 160개 단어 카드 및 18개 문법 퀴즈는 로그인 없이 iOS / iPadOS 17.0+ 기기에서 오프라인으로 작동합니다."),
            ("음성 롤플레이 및 오프라인 번역 팩 다운로드", "기기 내 시스템 언어 대화 모델은 iOS / iPadOS 26.0+ 호환 기기에서 동작하며 모든 iOS 17+ 기기에서 힌트 기반 연습이 가능합니다. 출국 전 iOS 설정 → 앱 → 번역에서 오프라인 언어 팩을 받아두세요."),
            ("$3.99 1회 평생 잠금해제 및 복원", "모든 앱은 무료 기본 기능과 $3.99 단일 평생 구매 옵션을 제공합니다(구독 없음). 다른 기기에서도 '구매 복원'으로 복원됩니다."),
            ("개발자 직접 지원", "help@appengine.fun으로 문의하시면 보통 24시간 내에 답변드립니다."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
    },
    "es": {
        "html_lang": "es",
        "title": "AE Languages — 5 Apps de Idiomas para Viajar | iPhone e iPad",
        "desc": "Descubre las 5 apps nativas de idiomas para viajar de AE Interactive: NihonGo, EnglishGo, EspanolGo, KoreanGo y MandarinGo. 500 vídeos reales de viaje, fonética interactiva, práctica oral guiada e intérprete en vivo sin registro.",
        "keywords": "AE Interactive,NihonGo,EnglishGo,EspanolGo,KoreanGo,MandarinGo,idiomas viaje,japones,ingles,espanol,coreano,mandarin",
        "brand_name": "AE Languages",
        "nav_apps": "5 Apps",
        "nav_compare": "Comparar Audio",
        "nav_matrix": "Comparativa",
        "nav_privacy": "Privacidad",
        "nav_support": "Soporte",
        "nav_studio": "Estudio AE",
        "hero_badge": "5 APPS EN APP STORE · IPHONE, IPAD E IPHONE DUO · SIN CUENTAS NI ANUNCIOS",
        "hero_title": "Habla Frases Reales de Viaje en <span>5 Idiomas</span>",
        "hero_sub": "Japonés, inglés, español, coreano y mandarín: cada app está programada de forma nativa en Swift con 15 unidades, 100 vídeos reales de viaje, laboratorio de escritura y fonética, Práctica Oral en 12 escenas e Intérprete Bidireccional en Vivo.",
        "status_pill": "Las 5 apps ya disponibles en App Store · Gratis para siempre + Pro opcional de $3.99",
        "cta_primary": "Elige tu destino ↓",
        "cta_audio": "▶ Comparar 5 idiomas",
        "cta_matrix": "Ver catálogo completo ↓",
        "stat_items": [
            ("5", "Idiomas de viaje"),
            ("500", "Vídeos de viaje reales"),
            ("3,000+", "Audios nativos MP3"),
            ("60", "Escenas de voz guiada"),
            ("$0 / $3.99", "Gratis + Pago único Pro"),
        ],
        "picker_badge": "¿CUÁL ES TU PRÓXIMO DESTINO?",
        "picker_title": "Elige un idioma para escuchar y ver la app por dentro",
        "picker_sub": "Toca cualquier idioma para escuchar los MP3 reales integrados en cada app, explorar capturas reales de iPhone y abrir App Store o su web oficial.",
        "btn_appstore_sub": "Descárgalo gratis en",
        "btn_appstore_main": "App Store",
        "btn_site": "Abrir sitio oficial →",
        "btn_play": "Reproducir",
        "btn_playing": "Sonando",
        "btn_focus": "Ver arriba ↑",
        "cmp_badge": "MISMO MOMENTO · CINCO IDIOMAS",
        "cmp_title": "Escucha cómo pedir la cuenta o pagar con tarjeta en 5 idiomas",
        "cmp_sub": "Clips MP3 extraídos directamente de NihonGo, EnglishGo, EspanolGo, KoreanGo y MandarinGo (acentos de Taiwán y China continental).",
        "grid_badge": "CATÁLOGO TRAVEL LANGUAGE GO",
        "grid_title": "Las 5 Apps Nativas para iPhone e iPad",
        "grid_sub": "Comienza gratis con tablas de sonidos completas, 24 pares mínimos, 160 tarjetas SM-2, Unidades 1–3 y 10 vídeos reales; desbloquea todo para siempre con un pago único de $3.99.",
        "matrix_badge": "COMPARATIVA LADO A LADO",
        "matrix_title": "Misma claridad a una mano. Cada idioma al detalle.",
        "matrix_cols": ["App", "Idioma", "Escritura y Fonética", "Especialidad Regional / Fonética", "Vídeos · Voz · Tarjetas", "Precio"],
        "matrix_common": "15 lecc. · 100 vídeos · 12 escenas · 160 tarjetas · Voz 2 vías",
        "matrix_price": "Gratis · $3.99 Pro",
        "pillars_badge": "ARQUITECTURA COMPARTIDA AE INTERACTIVE",
        "pillars_title": "Pensadas para aeropuertos, cafés, metro y hoteles reales",
        "pillars": [
            ("🎬", "100 Vídeos Reales por App (500 en total)", "Escenas ordenadas desde el aterrizaje hasta emergencias, con 200 grabaciones nativas, transcripción e IPA."),
            ("💬", "Práctica Oral en 12 Escenarios Reales", "El personal local inicia la conversación y tus pistas útiles permanecen visibles en pantalla mientras hablas."),
            ("🗣️", "Intérprete Bidireccional en Vivo", "Habla o escribe entre tu idioma y japonés, inglés, español, coreano o mandarín con tarjeta a pantalla completa."),
            ("🔒", "Sin Registro · Privacidad Total Local", "Sin cuentas, sin anuncios ni rastreadores de terceros. Tu progreso permanece únicamente en Apple UserDefaults."),
        ],
        "privacy_title": "Política de Privacidad — AE Travel Language Series",
        "privacy_updated": "Última actualización: 26 de noviembre de 2026",
        "privacy_sections": [
            ("1. Cero Rastreadores en este Portal y las 5 Apps", "languages.appengine.fun está operada por AE Interactive. Este sitio no utiliza cookies de seguimiento ni scripts publicitarios o analíticos, compartiendo el compromiso de cero recopilación de datos de NihonGo, EnglishGo, EspanolGo, KoreanGo y MandarinGo (NSPrivacyTracking = false)."),
            ("2. Progreso Local y Marcos Nativos de Apple", "Tus tarjetas SRS, trazos y ajustes se guardan localmente mediante Apple UserDefaults (CA92.1). La práctica oral y traducción bidireccional utilizan marcos nativos de Apple en el dispositivo sin cuentas externas."),
            ("3. Políticas de Privacidad Individuales", "También puedes consultar nihongo.appengine.fun/privacy, englishgo.appengine.fun/privacy, espanolgo.appengine.fun/privacy, koreango.appengine.fun/privacy y mandaringo.appengine.fun/privacy."),
            ("4. Contacto", "Para cualquier consulta escríbenos a help@appengine.fun."),
        ],
        "support_title": "Soporte y Compatibilidad — AE Languages",
        "support_sub": "Requisitos de compatibilidad, paquetes de traducción offline y contacto directo para las 5 apps.",
        "support_cards": [
            ("Cursos Offline, Vídeos y Tarjetas", "Todas las unidades, los 100 vídeos por app, tablas fonéticas, lienzo de escritura, 160 tarjetas SM-2 y 18 ejercicios funcionan offline en iOS / iPadOS 17.0+ sin crear cuenta."),
            ("Práctica Oral y Traducción Offline", "El diálogo en el dispositivo usa el modelo de lenguaje del sistema de Apple en iOS / iPadOS 26.0+ (con guía por frases en todos los iOS 17+). Descarga los paquetes offline en Ajustes de iOS → Apps → Traducir antes de viajar."),
            ("Pago Único de $3.99 De Por Vida y Restauración", "Cada app ofrece una amplia versión gratuita permanente y mejora opcional de $3.99 (sin suscripciones). Pulsa Restaurar compras en cualquier dispositivo con tu Apple ID."),
            ("Soporte Directo AE Interactive", "Escríbenos a help@appengine.fun (respuesta habitual en menos de 24 horas) o consulta la web dedicada de cada app."),
        ],
        "footer_rights": "© 2026 AE Interactive. Todos los derechos reservados.",
    },
}

CSS = """
:root {
  --bg: #070913;
  --card: rgba(18, 22, 40, 0.88);
  --border: rgba(255, 255, 255, 0.11);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --indigo: #818CF8;
  --teal: #2DD4BF;
  --coral: #FB7185;
  --amber: #F59E0B;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Apple SD Gothic Neo", "PingFang TC", "PingFang SC", "Hiragino Sans", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 42% at 50% -6%, rgba(129, 140, 248, 0.24) 0%, transparent 70%),
    radial-gradient(circle at 86% 14%, rgba(45, 212, 191, 0.14) 0%, transparent 45%),
    radial-gradient(circle at 12% 35%, rgba(251, 113, 133, 0.10) 0%, transparent 40%);
  background-repeat: no-repeat;
}
a { color: inherit; }
header { position: sticky; top: 12px; z-index: 100; padding: 0 16px; }
nav {
  max-width: 1060px; margin: 0 auto; padding: 10px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  background: rgba(11, 14, 28, 0.86);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border); border-radius: 999px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.45);
}
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 850; font-size: 16.5px; letter-spacing: -0.3px; }
.brand img { width: 34px; height: 34px; border-radius: 9px; border: 1px solid rgba(45, 212, 191, 0.45); }
.nav-right { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav-links { display: flex; gap: 14px; font-size: 13px; font-weight: 600; color: var(--muted); }
.nav-links a { text-decoration: none; transition: color .18s; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.lang-picker {
  display: flex; align-items: center; gap: 3px; flex-wrap: wrap;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
  padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.lang-picker a { color: var(--muted); text-decoration: none; padding: 2px 6px; border-radius: 99px; }
.lang-picker a.active { color: var(--teal); background: rgba(45,212,191,0.14); }
.nav-cta {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; text-decoration: none;
  font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}
main { max-width: 1060px; margin: 0 auto; padding: 34px 18px 72px; }
.hero { text-align: center; padding: 18px 0 28px; }
.badge {
  display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: 0.7px;
  color: var(--teal); background: rgba(45,212,191,0.12);
  border: 1px solid rgba(45,212,191,0.34); padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
h1 { font-size: clamp(30px, 5.2vw, 52px); font-weight: 900; letter-spacing: -1.1px; line-height: 1.12; margin-bottom: 14px; text-wrap: balance; }
h1 span { background: linear-gradient(125deg, #818CF8 0%, #2DD4BF 54%, #FB7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { max-width: 720px; margin: 0 auto 20px; color: var(--muted); font-size: clamp(15px, 2vw, 17.5px); text-wrap: balance; }
.status-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 999px;
  background: rgba(99,102,241,0.14); border: 1px solid rgba(99,102,241,0.38);
  color: #C7D2FE; font-size: 13px; font-weight: 700; margin-bottom: 20px;
}
.hero-icons { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; margin-bottom: 22px; }
.hero-ic-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px 6px 6px; border-radius: 999px;
  background: rgba(255,255,255,0.06); border: 1px solid var(--border); text-decoration: none;
  font-size: 13px; font-weight: 750; transition: transform .16s, border-color .16s;
}
.hero-ic-pill:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.32); }
.hero-ic-pill img { width: 28px; height: 28px; border-radius: 7px; }
.hero-cta { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 11px 20px; border-radius: 999px;
  font-size: 14px; font-weight: 750; text-decoration: none; border: 1px solid transparent; cursor: pointer;
  transition: transform .16s, box-shadow .16s, background .16s;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; box-shadow: 0 10px 26px rgba(99,102,241,0.32); }
.btn-ghost { background: rgba(255,255,255,0.06); border-color: var(--border); color: #E2E8F0; }
.btn-appstore {
  background: #fff; color: #090D16; border: 1px solid rgba(255,255,255,0.9);
  padding: 8px 18px; gap: 9px; box-shadow: 0 10px 26px rgba(255,255,255,0.12);
}
.btn-appstore svg { width: 18px; height: 22px; fill: currentColor; flex-shrink: 0; }
.btn-appstore .as-copy { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.12; text-align: left; }
.btn-appstore .as-sub { font-size: 9.5px; font-weight: 700; opacity: 0.72; }
.btn-appstore .as-main { font-size: 14.5px; font-weight: 850; }
.stat-bar {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;
  margin-top: 28px; padding: 16px; border-radius: 20px;
  background: var(--card); border: 1px solid var(--border);
}
.stat-cell { text-align: center; padding: 6px 4px; }
.stat-val { font-size: clamp(20px, 3vw, 28px); font-weight: 900; color: #fff; letter-spacing: -0.5px; }
.stat-lbl { font-size: 12px; font-weight: 650; color: var(--muted); margin-top: 2px; }
section { margin-top: 56px; }
.sec-head { text-align: center; margin-bottom: 24px; }
.sec-head .badge { margin-bottom: 10px; }
h2 { font-size: clamp(22px, 3.6vw, 34px); font-weight: 850; letter-spacing: -0.6px; margin-bottom: 8px; }
.sec-sub { color: var(--muted); max-width: 660px; margin: 0 auto; font-size: 15px; }
.picker-tabs { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
.dest-tab {
  display: inline-flex; align-items: center; gap: 8px; padding: 9px 16px 9px 10px; border-radius: 999px;
  background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: #CBD5E1;
  font-size: 13.5px; font-weight: 750; cursor: pointer; transition: all .18s ease;
}
.dest-tab img { width: 26px; height: 26px; border-radius: 7px; }
.dest-tab:hover { border-color: rgba(255,255,255,0.3); color: #fff; }
.dest-tab.active {
  background: var(--tab-soft, rgba(45,212,191,0.16));
  border-color: var(--tab-accent, var(--teal));
  color: #fff;
  box-shadow: 0 8px 22px rgba(0,0,0,0.35);
}
.spot-panel {
  display: none; background: var(--card); border: 1px solid var(--border);
  border-radius: 26px; padding: 24px; gap: 22px; flex-direction: column;
  box-shadow: 0 20px 50px rgba(0,0,0,0.45);
}
.spot-panel.active { display: flex; border-color: var(--spot-accent, var(--border)); }
.spot-top { display: flex; justify-content: space-between; align-items: center; gap: 18px; flex-wrap: wrap; }
.spot-id { display: flex; align-items: center; gap: 16px; max-width: 620px; }
.spot-id img { width: 72px; height: 72px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.22); box-shadow: 0 10px 24px rgba(0,0,0,0.4); }
.spot-kicker { font-size: 12px; font-weight: 800; letter-spacing: 0.4px; margin-bottom: 3px; }
.spot-id h3 { font-size: 24px; font-weight: 900; color: #fff; margin-bottom: 4px; }
.spot-id p { font-size: 14px; color: var(--muted); }
.spot-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.spot-specs { display: flex; gap: 8px; flex-wrap: wrap; }
.spec-pill {
  padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;
  background: rgba(255,255,255,0.06); border: 1px solid var(--border); color: #E2E8F0;
}
.spot-body { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1.25fr); gap: 18px; align-items: start; }
.spot-audios { display: flex; flex-direction: column; gap: 12px; }
.spot-shots { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
.mini-shot { background: rgba(7,9,19,0.7); border: 1px solid var(--border); border-radius: 16px; padding: 6px; }
.mini-shot img { width: 100%; height: auto; border-radius: 11px; display: block; }
.audio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 14px; }
.audio-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
  transition: border-color .2s, transform .2s;
}
.audio-card.playing { border-color: var(--teal); box-shadow: 0 0 0 1px rgba(45,212,191,0.35), 0 12px 28px rgba(0,0,0,0.4); }
.audio-tag { font-size: 11px; font-weight: 750; color: var(--teal); letter-spacing: 0.3px; }
.audio-phrase { font-size: 17.5px; font-weight: 850; margin-top: 5px; color: #fff; }
.audio-phonetic { font-size: 12.5px; color: #67E8F9; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-top: 4px; }
.audio-phonetic b { background: rgba(251, 113, 133, 0.2); color: #FDA4AF; padding: 0 4px; border-radius: 4px; }
.audio-meaning { font-size: 13px; color: var(--muted); margin-top: 5px; }
.play-btn {
  align-self: flex-start; background: rgba(99,102,241,0.22); color: #C7D2FE; border: 1px solid rgba(99,102,241,0.45);
  padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 750; cursor: pointer;
}
.audio-card.playing .play-btn { background: var(--teal); color: #042F2E; border-color: var(--teal); }
.apps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
.app-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 20px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 16px;
}
.app-card-head { display: flex; align-items: center; gap: 14px; }
.app-card-head img { width: 56px; height: 56px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.18); }
.app-card-kicker { font-size: 11px; font-weight: 800; letter-spacing: 0.4px; }
.app-card-head h3 { font-size: 19px; font-weight: 850; color: #fff; }
.app-card p { font-size: 13.5px; color: var(--muted); }
.app-card-links { display: flex; flex-wrap: wrap; gap: 8px; }
.app-card-links .btn { padding: 7px 13px; font-size: 12.5px; }
.matrix-wrap { overflow-x: auto; border-radius: 20px; border: 1px solid var(--border); background: var(--card); }
table { width: 100%; border-collapse: collapse; min-width: 720px; font-size: 13.5px; }
th, td { text-align: left; padding: 13px 14px; border-bottom: 1px solid rgba(255,255,255,0.07); }
th { font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: var(--teal); background: rgba(255,255,255,0.03); }
tr:last-child td { border-bottom: none; }
.td-app { display: flex; align-items: center; gap: 10px; font-weight: 800; color: #fff; }
.td-app img { width: 28px; height: 28px; border-radius: 7px; }
.bento { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }
.bento-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
.bento-icon { font-size: 24px; margin-bottom: 10px; }
.bento-card h3 { font-size: 16.5px; font-weight: 800; margin-bottom: 6px; color: #fff; }
.bento-card p { font-size: 13.5px; color: var(--muted); }
.doc-box { max-width: 820px; margin: 14px auto; background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 28px; }
.doc-box h1 { font-size: clamp(24px, 4vw, 36px); text-align: left; }
.doc-item { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--border); }
.doc-item h2 { font-size: 18px; margin-bottom: 6px; color: #E2E8F0; }
.doc-item p { font-size: 14.5px; color: var(--muted); }
footer {
  max-width: 1060px; margin: 42px auto 0; padding: 24px 18px 42px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 13px;
}
footer a { color: #CBD5E1; text-decoration: none; }
footer a:hover { color: var(--teal); }
@media (max-width: 820px) {
  .spot-body { grid-template-columns: 1fr; }
}
@media (max-width: 680px) {
  nav { border-radius: 22px; padding: 10px 14px; }
  .hero-cta .btn { width: 100%; justify-content: center; max-width: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn, .audio-card, .dest-tab { transition: none; }
}
"""

SCRIPT_JS = """
const audioMap = {};
let activeKey = null;
function togglePhrase(key, src, btnEl, cardEl, playLabel, playingLabel) {
  if (activeKey && activeKey !== key && audioMap[activeKey]) {
    audioMap[activeKey].audio.pause();
    audioMap[activeKey].audio.currentTime = 0;
    audioMap[activeKey].btn.textContent = "▶ " + audioMap[activeKey].playLabel;
    audioMap[activeKey].card.classList.remove("playing");
  }
  let item = audioMap[key];
  if (!item) {
    const a = new Audio(src);
    item = { audio: a, btn: btnEl, card: cardEl, playLabel: playLabel };
    a.addEventListener("ended", () => {
      btnEl.textContent = "▶ " + playLabel;
      cardEl.classList.remove("playing");
      if (activeKey === key) activeKey = null;
    });
    audioMap[key] = item;
  }
  if (!item.audio.paused) {
    item.audio.pause();
    item.audio.currentTime = 0;
    btnEl.textContent = "▶ " + playLabel;
    cardEl.classList.remove("playing");
    activeKey = null;
  } else {
    item.audio.play();
    btnEl.textContent = "■ " + playingLabel;
    cardEl.classList.add("playing");
    activeKey = key;
  }
}
function selectApp(slug) {
  document.querySelectorAll(".dest-tab").forEach((b) => {
    const on = b.dataset.slug === slug;
    b.classList.toggle("active", on);
    b.setAttribute("aria-selected", on ? "true" : "false");
  });
  document.querySelectorAll(".spot-panel").forEach((p) => {
    p.classList.toggle("active", p.dataset.slug === slug);
  });
}
window.addEventListener("DOMContentLoaded", () => {
  const h = (window.location.hash || "").replace("#", "");
  if (["nihongo", "englishgo", "espanolgo", "koreango", "mandaringo"].includes(h)) {
    selectApp(h);
  }
});
"""


def appstore_badge_svg() -> str:
    return '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def appstore_button(url: str, sub: str, main: str) -> str:
    return (
        f'<a class="btn btn-appstore" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'{appstore_badge_svg()}'
        f'<span class="as-copy"><span class="as-sub">{html_mod.escape(sub)}</span>'
        f'<span class="as-main">{html_mod.escape(main)}</span></span></a>'
    )


def nav_html(lang: str, route: str, t: dict) -> str:
    lang_links = []
    for code, label in LANG_LABELS:
        cls = ' class="active"' if code == lang else ""
        lang_links.append(f'<a href="{route}?lang={code}"{cls}>{label}</a>')
    p_cls = ' class="active"' if route == "/privacy" else ""
    s_cls = ' class="active"' if route == "/support" else ""
    q = f"?lang={lang}"
    return f"""
<header>
  <nav aria-label="Main navigation">
    <a class="brand" href="/{q}">
      <img src="/images/icon.webp" alt="AE Languages" width="34" height="34">
      <span>{html_mod.escape(t['brand_name'])}</span>
    </a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/{q}#spotlight">{html_mod.escape(t['nav_apps'])}</a>
        <a href="/{q}#compare">{html_mod.escape(t['nav_compare'])}</a>
        <a href="/{q}#matrix">{html_mod.escape(t['nav_matrix'])}</a>
        <a href="/privacy{q}"{p_cls}>{html_mod.escape(t['nav_privacy'])}</a>
        <a href="/support{q}"{s_cls}>{html_mod.escape(t['nav_support'])}</a>
      </div>
      <div class="lang-picker" role="navigation" aria-label="Language">{''.join(lang_links)}</div>
      <a class="nav-cta" href="https://appengine.fun/?lang={lang if lang in ('en','zh-Hant','zh-Hans','es') else 'en'}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['nav_studio'])}</a>
    </div>
  </nav>
</header>"""


def footer_html(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    app_links = " ".join(
        f'<a href="{a["website_url"]}" target="_blank" rel="noopener noreferrer">{a["name"]}</a>'
        for a in APPS
    )
    return f"""
<footer>
  <div>{html_mod.escape(t['footer_rights'])}</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;">
    {app_links}
    <a href="/privacy{q}">{html_mod.escape(t['nav_privacy'])}</a>
    <a href="/support{q}">{html_mod.escape(t['nav_support'])}</a>
    <a href="https://appengine.fun" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['nav_studio'])}</a>
    <a href="mailto:help@appengine.fun">help@appengine.fun</a>
  </div>
</footer>"""


def head_html(lang: str, t: dict, title: str, canonical_path: str) -> str:
    q = f"?lang={lang}" if lang != "en" else ""
    item_list = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "url": f"{ORIGIN}{canonical_path}{q}",
        "publisher": {"@type": "Organization", "name": "AE Interactive", "url": "https://appengine.fun"},
        "hasPart": [
            {
                "@type": "SoftwareApplication",
                "name": a["name"],
                "operatingSystem": "iOS 17.0+, iPadOS 17.0+",
                "applicationCategory": "EducationApplication",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "downloadUrl": a["app_store_url"],
                "sameAs": a["website_url"],
            }
            for a in APPS
        ],
    }
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{canonical_path}?lang={code}">\n'
        for code in LANG_ORDER
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(t['desc'])}">
<meta name="keywords" content="{html_mod.escape(t['keywords'])}">
<meta name="theme-color" content="#070913">
<link rel="canonical" href="{ORIGIN}{canonical_path}{q}">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{canonical_path}">
<link rel="icon" type="image/png" href="/images/icon.png">
<link rel="apple-touch-icon" href="/images/icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(t['desc'])}">
<meta property="og:url" content="{ORIGIN}{canonical_path}{q}">
<meta property="og:image" content="{ORIGIN}/images/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ORIGIN}/images/og.png">
<script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>"""


def audio_card_html(card_key: str, file_name: str, tag: str, phrase: str, phonetic: str, meaning: str, play_lbl: str, playing_lbl: str) -> str:
    p_esc = html_mod.escape(play_lbl)
    ing_esc = html_mod.escape(playing_lbl)
    return f"""
<article class="audio-card" id="card-{card_key}">
  <div>
    <div class="audio-tag">{html_mod.escape(tag)}</div>
    <div class="audio-phrase">{html_mod.escape(phrase)}</div>
    <div class="audio-phonetic">{phonetic}</div>
    <div class="audio-meaning">{html_mod.escape(meaning)}</div>
  </div>
  <button type="button" class="play-btn" onclick="togglePhrase('{card_key}','/audio/{file_name}',this,document.getElementById('card-{card_key}'),'{p_esc}','{ing_esc}')">▶ {p_esc}</button>
</article>"""


def build_home(lang: str, t: dict) -> str:
    hero_pills = "".join(
        f'<a class="hero-ic-pill" href="#{a["slug"]}" onclick="selectApp(\'{a["slug"]}\')">'
        f'<img src="/images/icon_{a["slug"]}.webp" alt="{a["name"]}" width="28" height="28">'
        f'<span>{html_mod.escape(a["name"])}</span></a>'
        for a in APPS
    )
    stat_cells = "".join(
        f'<div class="stat-cell"><div class="stat-val">{html_mod.escape(v)}</div><div class="stat-lbl">{html_mod.escape(l)}</div></div>'
        for v, l in t["stat_items"]
    )
    picker_tabs = []
    spot_panels = []
    for idx, app in enumerate(APPS):
        slug = app["slug"]
        active_cls = " active" if idx == 0 else ""
        selected_attr = "true" if idx == 0 else "false"
        picker_tabs.append(
            f'<button type="button" role="tab" aria-selected="{selected_attr}" '
            f'class="dest-tab{active_cls}" data-slug="{slug}" '
            f'style="--tab-accent:{app["accent"]};--tab-soft:{app["accent_soft"]};" '
            f'onclick="selectApp(\'{slug}\')">'
            f'<img src="/images/icon_{slug}.webp" alt="{app["name"]}" width="26" height="26">'
            f'<span>{app["flag"]} {html_mod.escape(app["pill_label"][lang])}</span></button>'
        )
        specs_html = "".join(f'<span class="spec-pill">{html_mod.escape(s)}</span>' for s in app["specs"][lang])
        audios_html = "".join(
            audio_card_html(
                f"sp-{slug}-{i}",
                au["file"],
                au["tag"][lang],
                au["phrase"],
                au["phonetic"],
                au["meaning"][lang],
                t["btn_play"],
                t["btn_playing"],
            )
            for i, au in enumerate(app["audios"])
        )
        shots_html = "".join(
            f'<div class="mini-shot"><img src="/images/{slug}_s{n}.webp" alt="{app["name"]} preview {n}" loading="lazy" width="420" height="912"></div>'
            for n in (1, 2, 3)
        )
        store_btn = appstore_button(app["app_store_url"], t["btn_appstore_sub"], t["btn_appstore_main"])
        spot_panels.append(f"""
        <article class="spot-panel{active_cls}" id="{slug}" data-slug="{slug}" style="--spot-accent:{app['accent']};">
          <div class="spot-top">
            <div class="spot-id">
              <img src="/images/icon_{slug}.webp" alt="{app['name']}" width="72" height="72">
              <div>
                <div class="spot-kicker" style="color:{app['accent']};">{app['flag']} {html_mod.escape(app['pill_label'][lang])} · v{app['version']}</div>
                <h3>{html_mod.escape(app['title'][lang])}</h3>
                <p>{html_mod.escape(app['tagline'][lang])}</p>
              </div>
            </div>
            <div class="spot-actions">
              {store_btn}
              <a class="btn btn-ghost" href="{app['website_url']}/?lang={lang if lang != 'en' else 'en'}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['btn_site'])}</a>
            </div>
          </div>
          <div class="spot-specs">{specs_html}</div>
          <div class="spot-body">
            <div class="spot-audios">{audios_html}</div>
            <div class="spot-shots">{shots_html}</div>
          </div>
        </article>""")

    cmp_cards = "".join(
        audio_card_html(
            f"cmp-{idx}",
            c["file"],
            f"{c['app_name']} · {c['lang_badge']}",
            c["phrase"],
            c["phonetic"],
            c["meaning"][lang],
            t["btn_play"],
            t["btn_playing"],
        )
        for idx, c in enumerate(COMPARISON_ITEMS)
    )

    grid_cards = []
    for app in APPS:
        slug = app["slug"]
        site_q = f"{app['website_url']}/?lang={lang}" if lang != "en" else app["website_url"]
        grid_cards.append(f"""
        <article class="app-card">
          <div>
            <div class="app-card-head">
              <img src="/images/icon_{slug}.webp" alt="{app['name']}" width="56" height="56">
              <div>
                <div class="app-card-kicker" style="color:{app['accent']};">{app['flag']} {html_mod.escape(app['pill_label'][lang])}</div>
                <h3>{html_mod.escape(app['name'])}</h3>
              </div>
            </div>
            <p style="margin-top:12px;">{html_mod.escape(app['tagline'][lang])}</p>
          </div>
          <div class="app-card-links">
            <a class="btn btn-primary" href="{app['app_store_url']}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['btn_appstore_main'])}</a>
            <a class="btn btn-ghost" href="{site_q}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['btn_site'])}</a>
            <a class="btn btn-ghost" href="#{slug}" onclick="selectApp('{slug}')">{html_mod.escape(t['btn_focus'])}</a>
          </div>
        </article>""")

    matrix_headers = "".join(f"<th>{html_mod.escape(c)}</th>" for c in t["matrix_cols"])
    matrix_rows = "".join(
        f"""<tr>
          <td><div class="td-app"><img src="/images/icon_{a['slug']}.webp" alt="{a['name']}" width="28" height="28"><span>{a['name']}</span></div></td>
          <td>{a['flag']} {html_mod.escape(a['pill_label'][lang].split('·')[0].strip())}</td>
          <td>{html_mod.escape(a['script_col'][lang])}</td>
          <td>{html_mod.escape(a['highlight_col'][lang])}</td>
          <td>{html_mod.escape(t['matrix_common'])}</td>
          <td>{html_mod.escape(t['matrix_price'])}</td>
        </tr>"""
        for a in APPS
    )

    pillar_cards = "".join(
        f"""<article class="bento-card">
          <div class="bento-icon" aria-hidden="true">{ic}</div>
          <h3>{html_mod.escape(ti)}</h3>
          <p>{html_mod.escape(bd)}</p>
        </article>"""
        for ic, ti, bd in t["pillars"]
    )

    return f"""{head_html(lang, t, t['title'], '/')}
<body>
{nav_html(lang, '/', t)}
<main>
  <section class="hero" style="margin-top:0;">
    <div class="badge">{html_mod.escape(t['hero_badge'])}</div>
    <h1>{t['hero_title']}</h1>
    <p class="hero-sub">{html_mod.escape(t['hero_sub'])}</p>
    <div class="status-pill"> {html_mod.escape(t['status_pill'])}</div>
    <div class="hero-icons">{hero_pills}</div>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#spotlight">{html_mod.escape(t['cta_primary'])}</a>
      <a class="btn btn-ghost" href="#compare">{html_mod.escape(t['cta_audio'])}</a>
      <a class="btn btn-ghost" href="#apps">{html_mod.escape(t['cta_matrix'])}</a>
    </div>
    <div class="stat-bar">{stat_cells}</div>
  </section>

  <section id="spotlight">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['picker_badge'])}</div>
      <h2>{html_mod.escape(t['picker_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['picker_sub'])}</p>
    </div>
    <div class="picker-tabs" role="tablist">{''.join(picker_tabs)}</div>
    {''.join(spot_panels)}
  </section>

  <section id="compare">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['cmp_badge'])}</div>
      <h2>{html_mod.escape(t['cmp_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['cmp_sub'])}</p>
    </div>
    <div class="audio-grid">{cmp_cards}</div>
  </section>

  <section id="apps">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['grid_badge'])}</div>
      <h2>{html_mod.escape(t['grid_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['grid_sub'])}</p>
    </div>
    <div class="apps-grid">{''.join(grid_cards)}</div>
  </section>

  <section id="matrix">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['matrix_badge'])}</div>
      <h2>{html_mod.escape(t['matrix_title'])}</h2>
    </div>
    <div class="matrix-wrap">
      <table>
        <thead><tr>{matrix_headers}</tr></thead>
        <tbody>{matrix_rows}</tbody>
      </table>
    </div>
  </section>

  <section>
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['pillars_badge'])}</div>
      <h2>{html_mod.escape(t['pillars_title'])}</h2>
    </div>
    <div class="bento">{pillar_cards}</div>
  </section>
</main>
{footer_html(lang, t)}
<script>{SCRIPT_JS}</script>
</body>
</html>"""


def build_doc_page(lang: str, t: dict, route: str, heading: str, sub: str, items: list[tuple[str, str]]) -> str:
    blocks = "".join(
        f'<div class="doc-item"><h2>{html_mod.escape(h)}</h2><p>{html_mod.escape(p)}</p></div>'
        for h, p in items
    )
    app_links = "".join(
        f'<a class="btn btn-ghost" style="padding:7px 14px;font-size:12.5px;" href="{a["website_url"]}{route}?lang={lang}" target="_blank" rel="noopener noreferrer">{a["flag"]} {a["name"]}</a>'
        for a in APPS
    )
    return f"""{head_html(lang, t, heading + ' | AE Languages', route)}
<body>
{nav_html(lang, route, t)}
<main>
  <article class="doc-box">
    <h1>{html_mod.escape(heading)}</h1>
    <p style="color:var(--teal);font-weight:700;font-size:14px;margin-top:8px;">{html_mod.escape(sub)}</p>
    {blocks}
    <div class="doc-item">
      <div style="display:flex;gap:10px;flex-wrap:wrap;">{app_links}</div>
    </div>
  </article>
</main>
{footer_html(lang, t)}
</body>
</html>"""


def cf_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def deploy_worker(token: str, worker_js: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    boundary = "----AELanguagesBoundary847261"
    body = [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="metadata"',
        b"Content-Type: application/json",
        b"",
        json.dumps({"main_module": "index.js", "compatibility_date": "2024-03-03"}).encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="index.js"; filename="index.js"',
        b"Content-Type: application/javascript+module",
        b"",
        worker_js.encode("utf-8"),
        f"--{boundary}--".encode(),
        b"",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(body),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read())
        assert res.get("success"), f"Worker upload failed: {res}"
        print("WORKER_UPLOADED:", SCRIPT_NAME)


def ensure_dns_and_route(token: str) -> None:
    dns = cf_request("GET", f"/zones/{ZONE_ID}/dns_records?name={HOSTNAME}", token)
    existing = dns.get("result", [])
    if not existing:
        created = cf_request("POST", f"/zones/{ZONE_ID}/dns_records", token, {
            "type": "A",
            "name": HOSTNAME,
            "content": "192.0.2.1",
            "proxied": True,
            "ttl": 1,
        })
        assert created.get("success"), f"DNS create failed: {created}"
        print("DNS_CREATED:", HOSTNAME)
    else:
        print("DNS_EXISTS:", [(r["type"], r["name"], r["content"], r["proxied"]) for r in existing])

    routes = cf_request("GET", f"/zones/{ZONE_ID}/workers/routes", token).get("result", [])
    pattern = f"{HOSTNAME}/*"
    match = [r for r in routes if r.get("pattern") == pattern]
    if not match:
        rc = cf_request("POST", f"/zones/{ZONE_ID}/workers/routes", token, {
            "pattern": pattern,
            "script": SCRIPT_NAME,
        })
        assert rc.get("success"), f"Route create failed: {rc}"
        print("ROUTE_CREATED:", pattern, "->", SCRIPT_NAME)
    else:
        rid = match[0]["id"]
        if match[0].get("script") != SCRIPT_NAME:
            cf_request("PUT", f"/zones/{ZONE_ID}/workers/routes/{rid}", token, {
                "pattern": pattern,
                "script": SCRIPT_NAME,
            })
            print("ROUTE_UPDATED:", pattern, "->", SCRIPT_NAME)
        else:
            print("ROUTE_EXISTS:", pattern, "->", SCRIPT_NAME)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-only", action="store_true", help="Build HTML & worker.js locally without uploading to Cloudflare")
    args = ap.parse_args()

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    pages, privacy_pages, support_pages = {}, {}, {}
    for code, t in CONTENT.items():
        home_html = build_home(code, t)
        priv_html = build_doc_page(code, t, "/privacy", t["privacy_title"], t["privacy_updated"], t["privacy_sections"])
        supp_html = build_doc_page(code, t, "/support", t["support_title"], t["support_sub"], t["support_cards"])
        pages[code] = home_html
        privacy_pages[code] = priv_html
        support_pages[code] = supp_html
        suffix = "" if code == "en" else f"_{code}"
        (PUBLIC_DIR / f"index{suffix}.html").write_text(home_html, encoding="utf-8")
        (PUBLIC_DIR / f"privacy{suffix}.html").write_text(priv_html, encoding="utf-8")
        (PUBLIC_DIR / f"support{suffix}.html").write_text(supp_html, encoding="utf-8")

    images = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(IMG_DIR.glob("*"))}
    audio = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(AUD_DIR.glob("*.mp3"))}

    sitemap_urls = "\n".join(
        [f"  <url><loc>{ORIGIN}/</loc><priority>1.0</priority></url>"]
        + [f"  <url><loc>{ORIGIN}/?lang={c}</loc><priority>0.9</priority></url>" for c in LANG_ORDER if c != "en"]
        + [f"  <url><loc>{ORIGIN}/privacy</loc><priority>0.7</priority></url>"]
        + [f"  <url><loc>{ORIGIN}/support</loc><priority>0.7</priority></url>"]
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>'
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"

    worker_js = f"""const PAGES = {json.dumps(pages)};
const PRIVACY_PAGES = {json.dumps(privacy_pages)};
const SUPPORT_PAGES = {json.dumps(support_pages)};
const IMAGES = {json.dumps(images)};
const AUDIO = {json.dumps(audio)};
const SITEMAP = {json.dumps(sitemap_xml)};
const ROBOTS = {json.dumps(robots_txt)};

function b64ToBytes(b64) {{
  const s = atob(b64);
  const out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}}

function resolveLang(request) {{
  const url = new URL(request.url);
  const q = url.searchParams.get("lang");
  if (q && PAGES[q]) return q;
  if (q === "zh-TW" || q === "tw" || q === "hk") return "zh-Hant";
  if (q === "zh-CN" || q === "cn" || q === "zh") return "zh-Hans";
  if (q === "jp" || q === "ja-JP") return "ja";
  if (q === "kr" || q === "ko-KR") return "ko";
  if (q === "es-ES" || q === "es-MX") return "es";
  const accept = (request.headers.get("accept-language") || "").toLowerCase();
  if (accept.includes("zh-tw") || accept.includes("zh-hk") || accept.includes("zh-hant")) return "zh-Hant";
  if (accept.includes("zh")) return "zh-Hans";
  if (accept.includes("ja")) return "ja";
  if (accept.includes("ko")) return "ko";
  if (accept.includes("es")) return "es";
  return "en";
}}

export default {{
  async fetch(request) {{
    const pathname = new URL(request.url).pathname;
    if (pathname === "/sitemap.xml") {{
      return new Response(SITEMAP, {{ headers: {{ "content-type": "application/xml;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname === "/robots.txt") {{
      return new Response(ROBOTS, {{ headers: {{ "content-type": "text/plain;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname.startsWith("/images/")) {{
      const name = pathname.slice("/images/".length);
      if (IMAGES[name]) {{
        const ct = name.endsWith(".png") ? "image/png" : "image/webp";
        return new Response(b64ToBytes(IMAGES[name]), {{ headers: {{ "content-type": ct, "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    if (pathname.startsWith("/audio/")) {{
      const name = pathname.slice("/audio/".length);
      if (AUDIO[name]) {{
        return new Response(b64ToBytes(AUDIO[name]), {{ headers: {{ "content-type": "audio/mpeg", "accept-ranges": "bytes", "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    const lang = resolveLang(request);
    const htmlHeaders = {{
      "content-type": "text/html;charset=UTF-8",
      "cache-control": "public, max-age=0, must-revalidate",
      "vary": "Accept-Language"
    }};
    if (pathname === "/privacy" || pathname === "/privacy.html") {{
      return new Response(PRIVACY_PAGES[lang] || PRIVACY_PAGES.en, {{ headers: htmlHeaders }});
    }}
    if (pathname === "/support" || pathname === "/support.html") {{
      return new Response(SUPPORT_PAGES[lang] || SUPPORT_PAGES.en, {{ headers: htmlHeaders }});
    }}
    return new Response(PAGES[lang] || PAGES.en, {{ headers: htmlHeaders }});
  }}
}};
"""
    (BASE_DIR / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"BUILT_WORKER: {len(worker_js) / 1024:.1f} KB ({len(images)} images, {len(audio)} audio)")

    if args.build_only:
        print("BUILD_ONLY_COMPLETE")
        return

    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        token = Path("~/.cf_token").expanduser().read_text().strip()
    deploy_worker(token, worker_js)
    ensure_dns_and_route(token)
    print("DEPLOY_COMPLETE:", ORIGIN)


if __name__ == "__main__":
    main()
