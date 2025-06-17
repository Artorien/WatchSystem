--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-24 11:52:58

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--


--
-- TOC entry 3386 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: captions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.captions (
    id bigint NOT NULL,
    text text NOT NULL,
    platform_source text NOT NULL,
    scrape_time text NOT NULL
);


ALTER TABLE public.captions OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: captions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.captions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.captions_id_seq OWNER TO postgres;

--
-- TOC entry 3387 (class 0 OID 0)
-- Dependencies: 217
-- Name: captions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.captions_id_seq OWNED BY public.captions.id;


--
-- TOC entry 220 (class 1259 OID 16400)
-- Name: intro_captions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.intro_captions (
    id integer NOT NULL,
    text character varying(255) NOT NULL
);


ALTER TABLE public.intro_captions OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16399)
-- Name: intro_captions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.intro_captions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.intro_captions_id_seq OWNER TO postgres;

--
-- TOC entry 3388 (class 0 OID 0)
-- Dependencies: 219
-- Name: intro_captions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.intro_captions_id_seq OWNED BY public.intro_captions.id;


--
-- TOC entry 222 (class 1259 OID 16407)
-- Name: played_captions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.played_captions (
    id integer NOT NULL,
    caption_id integer NOT NULL
);


ALTER TABLE public.played_captions OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16406)
-- Name: played_captions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.played_captions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.played_captions_id_seq OWNER TO postgres;

--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 221
-- Name: played_captions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.played_captions_id_seq OWNED BY public.played_captions.id;


--
-- TOC entry 3220 (class 2604 OID 16393)
-- Name: captions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.captions ALTER COLUMN id SET DEFAULT nextval('public.captions_id_seq'::regclass);


--
-- TOC entry 3221 (class 2604 OID 16403)
-- Name: intro_captions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intro_captions ALTER COLUMN id SET DEFAULT nextval('public.intro_captions_id_seq'::regclass);


--
-- TOC entry 3222 (class 2604 OID 16410)
-- Name: played_captions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.played_captions ALTER COLUMN id SET DEFAULT nextval('public.played_captions_id_seq'::regclass);


--
-- TOC entry 3376 (class 0 OID 16390)
-- Dependencies: 218
-- Data for Name: captions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.captions (id, text, platform_source, scrape_time) FROM stdin;
1	btc	✅ Long\n\n#ONG/USDT\n\nEntry zone : 0.170814 - 0.1743000\n\nTargets : 0.1755148 - 0.1789904 - 0.1824659 - 0.1859414 - 0.1894170 - 0.1928925 - 0.1963681 - 0.1998436\n\nStop loss :0.162099\n\nLeverage: 5x_10x\n\n#BTC #ROSE #TON #Ethereum #WIF #ETHUSDT #SAFE $SAFE\n\nhttps://t.co/CkZ0n503rt	Thu Apr 03 13:02:04 +0000 2025
2	btc	@Bstr___ Good Morning Bstr!  Have a great Thursday!	Thu Apr 03 13:02:03 +0000 2025
3	btc	BTC hashrate hits a new ATH. https://t.co/zSVAwmsqyt	Thu Apr 03 13:02:03 +0000 2025
4	btc	@keenn_eth GM legend	Thu Apr 03 13:02:02 +0000 2025
5	btc	@BBJieRan 可以的	Thu Apr 03 13:02:01 +0000 2025
6	btc	#Altcoins are falling to zero against #BTC \n#BTC to 70k	Thu Apr 03 13:02:01 +0000 2025
7	btc	@saylor BTC is freedom—no limits, no passport, fully decentralized! 🚀\n\nThe future will be split between those who own BTC and those who will never afford it because of its future price. 🔥	Thu Apr 03 13:02:01 +0000 2025
8	btc	@EylemCulculoglu Ya eylem 100 bin altı btc ucuz diyordun. 50 şey yazıyorsun biri tutunca ben dedim diyorsun. Hadi diğerleri ergen sen 50 yaşında adamsın utan biraz ak	Thu Apr 03 13:02:01 +0000 2025
9	btc	🚨 BTC &amp; ETH in Turbulence! 📉\n\n📌 Bitcoin surged to $88,500, but quickly dropped below $83K after tariff news.\n📌 Ethereum couldn't hold above $2K, with bears in control.\n⚡ The market awaits the next wave of volatility! Up or down? ⬇️ #Bitcoin #Ethereum #Crypto\n\nMore on👉 https://t.co/VmthkWEsJJ	Thu Apr 03 13:02:00 +0000 2025
10	btc	It's Buzzing! Our latest member gain is 1 0 0.02 % on $VINE ! Ready for your next big win ? Start your 14 -DAY FREE trial and join us now ! !  - https://t.co/ccaleYKuuA - Get in now! $ONDO $TRX $USDC $ADA $XRP $ETH $MNT $SOL $DOGE $BTC https://t.co/8J6OgegsxH	Thu Apr 03 13:02:00 +0000 2025
11	btc	📈 Bitcoin Surges Over 7%!\nAfter Trump delays tariffs by 90 days, crypto and related stocks rebound\nsoaring 7.64% in the past 24 hours.\n\nRead more in the comment.\n\n#Trendpro #TrendproGlobal #TradeWithTheBest #Bitcoin #CryptoNews #TrumpTariffs #BTC #MarketUpdate #InvestSmart https://t.co/lOpKbb4zjD	Thu Apr 10 08:11:12 +0000 2025
12	btc	@BD_GemX @grvt_io Setting the stage for something huge 🎭🚀	Thu Apr 10 08:11:11 +0000 2025
13	btc	@0xBclub @bcgame 你想回答内裤也可以	Thu Apr 10 08:11:11 +0000 2025
14	btc	@Alphafox78 maybe she has a jewish heritage?	Thu Apr 10 08:11:11 +0000 2025
15	btc	@Cruise_BTC Acha Hai	Thu Apr 10 08:11:10 +0000 2025
16	btc	LARGE WHALE MOVEMENT  \nAmount: 149.00 BTC ($12,170,022 USD)\nFrom:\n  + 1 Unknown(s)\nTo:\n  + 11 Unknown(s)\nTime: 08:11 AM UTC\n- @boomwatchapp #Bitcoin #BoomWatch	Thu Apr 10 08:11:10 +0000 2025
17	btc	合约就是赌博、\n玩合约就是嫌钱多！！！！，\n合约就是给交易所送钱。\n合约就是死路一条！！\n\n人家华尔街拿出100亿美金出来做市，\n操作20-30%还不是分分钟的事情。。\n\n可以明确的说。#btc 的大庄可以操控价格。。\n合约没有半点机会,K线无用！	Thu Apr 10 08:11:10 +0000 2025
18	btc	@VixenSlays Not just memes #humanize\nTg .X . Dex updated @Humanizesol \nCommunity claim\nReversal from 100k \n1,8 M——&gt; 100k\nNow 160k\nScreen we hit NEW ATH\n$sol $btc $eth #humanize\n\nhttps://t.co/GvOKKdxg5X	Thu Apr 10 08:11:09 +0000 2025
19	btc	Gold Sell : 3115 - 3118\n\nSl : 3121\n\nTp1 : 3105\nTp2 : 3095\n\n#EURUSD #FOREX #GBPUSD #XAUUSD\n#XAGUSD #GOLD #USDJPY #BTC https://t.co/3g2gozaIql	Thu Apr 10 08:11:07 +0000 2025
20	btc	binance just added 22,106 $BTC (worth $1.82b) to their reserves over last 12 days... macro uncertainty and upcoming CPI announcement got ppl movin their coins to exchanges ‌‌​​‌​‌‌​‌	Thu Apr 10 08:11:06 +0000 2025
21	ootd	@rejekianakbaik Ngeri juga damoaknya ya	Thu Apr 10 08:14:01 +0000 2025
22	ootd	@vanzhalay People come and gi	Thu Apr 10 08:13:52 +0000 2025
23	ootd	@ulahnetijen Jadi bahenil gitu	Thu Apr 10 08:13:38 +0000 2025
24	ootd	OOTD驾到 通通闪开📢\n（请不要在意我的拖鞋。）\n\n#일상계_트친소 #일상계트친소 https://t.co/nEHelRg7DX	Thu Apr 10 08:13:34 +0000 2025
25	ootd	@minmie_e Bgus ih lagunya	Thu Apr 10 08:13:25 +0000 2025
26	ootd	@bakeokbunda Ywdh gih sini	Thu Apr 10 08:13:16 +0000 2025
27	ootd	@frdlh___ Akun udh lupa lagunya	Thu Apr 10 08:13:07 +0000 2025
28	ootd	@threags Ya benr bgt	Thu Apr 10 08:12:58 +0000 2025
29	ootd	@threags Pasti sih kaa	Thu Apr 10 08:12:49 +0000 2025
30	ootd	@snxxrc Keren sih ini	Thu Apr 10 08:12:41 +0000 2025
31	snp500	10/10 🔑 Key takeaway:2025 tariffs provide investors with a unique lens to identify genuinely durable businesses—an opportunity wrapped in caution.\n#tarriffwar #tarrifs #Trump #TrumpRecession #TrumpMarketCrash #stockmarketcrash #StockMarketIndia #SNP500	Thu Apr 10 07:46:22 +0000 2025
32	snp500	@coaltown559 @MustStopMurad @goodalexander @snp500solana A major announcement is on the horizon. If you’re not in SnP500 yet, now’s the time. 🚀🔥	Thu Apr 10 07:43:11 +0000 2025
33	snp500	@coaltown559 @MustStopMurad @goodalexander @snp500solana Big moves are coming. The SnP500 journey is about to get even bigger. Are you ready? 👀🔥	Thu Apr 10 07:42:14 +0000 2025
34	snp500	@shayteonsol Memecoins are built on community. SnP500 is built different. Who’s here for the long ride? 💰🔥	Thu Apr 10 07:19:27 +0000 2025
35	snp500	@shayteonsol The world is waking up to SnP500. Are you ahead of the trend—or catching up? 🚀🔥	Thu Apr 10 07:18:41 +0000 2025
36	snp500	@J_Nice_ @pumpdotfun Some are still watching. Others are stacking. The real ones are already winning. 🚀🔥 SnP500	Thu Apr 10 06:50:15 +0000 2025
37	snp500	@J_Nice_ @pumpdotfun This isn’t just a coin. This is a financial revolution. And SnP500 is leading the way. 💰🔥	Thu Apr 10 06:49:28 +0000 2025
38	snp500	@J_Nice_ @pumpdotfun Hahah 100% \nWhole SNP500 community 🔥🔥	Thu Apr 10 06:42:28 +0000 2025
39	snp500	@ProjectLiberal What snp500 is doing these days I'd expect from a meme coin... US is now a meme.	Thu Apr 10 06:36:00 +0000 2025
40	snp500	@J_Nice_ One post, one retweet, one share. That’s all it takes to spread the movement. Let’s make SnP500 viral! 🚀🔥	Thu Apr 10 05:43:48 +0000 2025
41	nhl	Writing Scripts like I’m in Hollywood ⭐️ \n\nNHL (Tues)\nMLB (Wed) https://t.co/53crLq3tFJ	Thu Apr 10 08:18:26 +0000 2025
42	nhl	I love nhl hockey and hockeytwt I learned there's a hockey player literally named Flower that's the cutest thing ever	Thu Apr 10 08:18:20 +0000 2025
43	nhl	Food is the last thing we must appreciate for how it looks. \n\nFashion, devices, tech, products everything I get — food is supposed to be tasty and nutritious, I think too many new restaurants/stores are looking at making 'food look good' at exorbitant price points.	Thu Apr 10 08:18:14 +0000 2025
44	nhl	✅✅✅\n\nJoin Free Telegram: https://t.co/ASrY66SPED\n\n#GamblingX\n#GamblingX #sportsbettingpicks #FanDuel #prizepicks #NBA #CBB #nhl #HardRockBet #MLB #NHL #DraftKings https://t.co/5Mx6X7zfyy	Thu Apr 10 08:17:28 +0000 2025
45	nhl	PrizePicks MLB/NBA ⚾️🏀\n\nhttps://t.co/EZ5EvyudNj\n\n#PrizePicks #picks #prizepickslocks #prizepickslock #props #gambling #gamblingx #gamblingtwitter #bets #dfs   #gamblingcommunity #CFB #NFL  #nhl #UnderdogFantasy \n#NBA #nflbets https://t.co/JnRaUBaE5q	Thu Apr 10 08:16:52 +0000 2025
46	nhl	Cizinec, hokejista překonal rekord a stal se prvním v počtu gólů v NHL. Překonal tím slavného dalšího slavného hokejistu, cizince Wayna Gretzkyho. https://t.co/BMzabsj1DT	Thu Apr 10 08:15:15 +0000 2025
47	nhl	@NHL Wild's Gamble: Is This Move Suicide?\nhttps://t.co/SuBYamWICq	Thu Apr 10 08:14:50 +0000 2025
48	nhl	@PatBoyle44 Kudos from Western Canada for including an NHL achievement in your poll. \n#LetsGoOilers	Thu Apr 10 08:14:42 +0000 2025
49	nhl	@NHL @Energizer @leon_pustilnik	Thu Apr 10 08:13:51 +0000 2025
50	nhl	PrizePicks MLB/NBA ⚾️🏀\n\nhttps://t.co/ASrY66SPED\n\n#PrizePicks #picks #prizepickslocks #prizepickslock #props #gambling #gamblingx #gamblingtwitter #bets #dfs   #gamblingcommunity #CFB #NFL  #nhl #UnderdogFantasy \n#NBA #nflbets https://t.co/ue2pWebn8W	Thu Apr 10 08:13:47 +0000 2025
51	btc	@MrWhaleREAL btc buy big level	Thu Apr 10 08:20:46 +0000 2025
52	btc	@GraceNft89 Morning Queen. Happy Thursday	Thu Apr 10 08:20:45 +0000 2025
53	btc	@girlofsolana Haha Facts Lilith	Thu Apr 10 08:20:44 +0000 2025
54	btc	@Aurorawwwwww 发财了	Thu Apr 10 08:20:44 +0000 2025
55	btc	@CyrusAbrahimX Gm 🍎 Cyrus	Thu Apr 10 08:20:42 +0000 2025
56	btc	#POPCATUSDT\n\nEntry: 0.131\n\nTarget 1: 0.135✅\nTarget 2: 0.140✅\nTarget 3: 0.145\nTarget 4: 0.150\nTarget 5: 0.155\nTarget 6: 0.160\nTarget 7: 0.165\n\n#bitcoin #crypto #BTC #ETH #altcoin #trading #signal #copytrading #cryptosignal $POPCAT #POPCAT\nhttps://t.co/FFUBtObGqH	Thu Apr 10 08:20:42 +0000 2025
57	btc	#VINEUSDT\n\nEntry: 0.028\n\nTarget 1: 0.030✅\nTarget 2: 0.032✅\nTarget 3: 0.034✅\nTarget 4: 0.036\nTarget 5: 0.040\n\n#bitcoin #crypto #BTC #ETH #altcoin #trading #signal #copytrading #cryptosignal $VINE #VINE\nhttps://t.co/XTtebEvSTJ	Thu Apr 10 08:20:42 +0000 2025
58	btc	@rovercrc "ETRO BTC Layer 2 connects Bitcoin, is compatible with Ethereum's EVM, and links the blockchain world!\nETRO represents the original shares of the ETRO Bitcoin Layer 2 public blockchain. Owning ETRO means owning the fountain of wealth!"\n@https://t.me/ETROBTCZH\n@Etrobtc	Thu Apr 10 08:20:40 +0000 2025
59	btc	BTC/USD Forecast: Holds $75K As Support Level Gets Retested $BTC.X https://t.co/3nATPLqvDV	Thu Apr 10 08:20:39 +0000 2025
60	btc	@James_M_BTC @MEXC_Official Frauds	Thu Apr 10 08:20:39 +0000 2025
61	btc	@wimps GM GM	Thu Apr 10 09:55:07 +0000 2025
62	btc	Celebrate the 300% rise in $BTC this week!\n\nhttps://t.co/rRxJJ6yN2n\n\n$LUNA $APE $SEI $GNO $BLUR $ROSE $AR $ZEC $GAS $TWT $XAUT $GMX $CSPR $NEXO $HT $BTC $ETH $SATS $sol https://t.co/O6mP8iEigA	Thu Apr 10 09:55:06 +0000 2025
63	btc	Bitcoin Miners Scramble to Import Gear Before Tariffs Hit\nBTC: 81963 USD, 24h Change: 5.78%\nhttps://t.co/i4J9udGnyD	Thu Apr 10 09:55:06 +0000 2025
64	btc	🔁 Swap\n👤[5h72]: 0.896 $BTC → ⚡ → 37.9 $ETH ($69.0K)\nSlip: 6.780 %, liq. fee: $6.0K‼️\nhttps://t.co/oJMVUntQp9	Thu Apr 10 09:55:06 +0000 2025
65	btc	#TROYUSDT\n\nEntry: 0.00041\n\nTarget 1: 0.00045✅\nTarget 2: 0.00050\nTarget 3: 0.00055\nTarget 4: 0.00060\n\n#bitcoin #crypto #BTC #ETH #altcoin #trading #signal #copytrading #cryptosignal $TROY #TROY\nJoin our telegram community.\nClick below ⬇️https://t.co/vOijbF6X91	Thu Apr 10 09:55:05 +0000 2025
66	btc	@jiamihui 起飞	Thu Apr 10 09:55:04 +0000 2025
67	btc	@Gotzeuus People are happy because maybe they bought yesterday but let’s see when they will be in the inverse of insider trading.\n\nIf we have 4 years of this, we will all go to 0 😂	Thu Apr 10 09:55:04 +0000 2025
68	btc	@CryptoGirlNova btc's got that resilience, fam. keep an eye out, the ride ain't over yet.	Thu Apr 10 09:55:04 +0000 2025
69	btc	@Cruise_BTC Good morning dear	Thu Apr 10 09:55:03 +0000 2025
70	btc	@BobLoukas I don’t get it. You acknowledge yourself, correctly, that it was inevitable. \n\nWhat should people have done? Genuinely wondering. \n\nAlso, people being greedy/cheering on TradFi on X did not alter the course of BTC adoption history.	Thu Apr 10 09:55:03 +0000 2025
\.


--
-- TOC entry 3378 (class 0 OID 16400)
-- Dependencies: 220
-- Data for Name: intro_captions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.intro_captions (id, text) FROM stdin;
\.


--
-- TOC entry 3380 (class 0 OID 16407)
-- Dependencies: 222
-- Data for Name: played_captions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.played_captions (id, caption_id) FROM stdin;
\.


--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 217
-- Name: captions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.captions_id_seq', 70, true);


--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 219
-- Name: intro_captions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.intro_captions_id_seq', 1, false);


--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 221
-- Name: played_captions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.played_captions_id_seq', 1, false);


--
-- TOC entry 3224 (class 2606 OID 16397)
-- Name: captions captions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.captions
    ADD CONSTRAINT captions_pkey PRIMARY KEY (id);


--
-- TOC entry 3226 (class 2606 OID 16405)
-- Name: intro_captions intro_captions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intro_captions
    ADD CONSTRAINT intro_captions_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 16412)
-- Name: played_captions played_captions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.played_captions
    ADD CONSTRAINT played_captions_pkey PRIMARY KEY (id);


--
-- TOC entry 3229 (class 2606 OID 16413)
-- Name: played_captions caption_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.played_captions
    ADD CONSTRAINT caption_id FOREIGN KEY (caption_id) REFERENCES public.captions(id);


-- Completed on 2025-04-24 11:52:59

--
-- PostgreSQL database dump complete
--

