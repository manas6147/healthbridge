<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthBridge - Aceternity Master Edition</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                        serif: ['Playfair Display', 'serif'],
                    },
                    colors: {
                        darkBg: '#020617',
                        skyGlow: '#38bdf8',
                        indigoGlow: '#818cf8',
                    }
                }
            }
        }
    </script>
    <style>
        /* Base Styling */
        body {
            background-color: #020617;
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }

        /* Fixed Canvas Cloud Background Shader */
        #cloud-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            pointer-events: none;
        }

        /* Glassmorphism Bento Grid Card */
        .glass-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.2);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 25px 60px rgba(14, 165, 233, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        /* Aceternity Gooey Liquid Input */
        .gooey-input {
            background: rgba(15, 23, 42, 0.85);
            border: 2px solid rgba(56, 189, 248, 0.25);
            color: #ffffff;
            border-radius: 16px;
            padding: 12px 20px;
            outline: none;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.08);
        }

        .gooey-input:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.4), inset 0 0 10px rgba(56, 189, 248, 0.2);
            transform: scale(1.01);
        }

        /* Magnetic & Glow Buttons */
        .magnetic-btn {
            background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
            color: #ffffff;
            font-weight: 600;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 24px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.35);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            cursor: pointer;
        }

        .magnetic-btn:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #4f46e5 100%);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 35px rgba(56, 189, 248, 0.6);
        }

        .magnetic-btn:active {
            transform: translateY(1px) scale(0.98);
        }

        /* Floating Dock Styling */
        .dock-container {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 24px;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 9999px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(56, 189, 248, 0.2);
            z-index: 9999;
        }

        .dock-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #94a3b8;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
        }

        .dock-btn:hover {
            transform: scale(1.3) translateY(-8px);
            background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.6);
            box-shadow: 0 10px 25px rgba(56, 189, 248, 0.6);
        }

        .dock-btn.active {
            background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
            color: #ffffff;
            border-color: rgba(56, 189, 248, 0.8);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        }

        .dock-tooltip {
            position: absolute;
            top: -42px;
            left: 50%;
            transform: translateX(-50%) scale(0.8);
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #f8fafc;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: all 0.2s ease;
        }

        .dock-btn:hover .dock-tooltip {
            opacity: 1;
            transform: translateX(-50%) scale(1);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #020617;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #38bdf8;
        }
    </style>
</head>
<body class="min-h-screen text-slate-100 pb-32 selection:bg-sky-500 selection:text-white">

    <!-- Fixed Atmospheric Cloud Shader Canvas -->
    <canvas id="cloud-canvas"></canvas>

    <!-- Top Navigation Header -->
    <header class="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/60 border-b border-sky-500/10 px-6 py-4">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3 cursor-pointer" onclick="switchPage('home')">
                <div class="p-2.5 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 text-white shadow-lg shadow-sky-500/30">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                    <h1 class="text-xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-300 to-indigo-300">HealthBridge</h1>
                    <p class="text-xs text-sky-400/80 font-medium tracking-wide">ACETERNITY MASTER EDITION</p>
                </div>
            </div>

            <!-- Global Live Alert Center Popover -->
            <div class="relative">
                <button id="notif-btn" onclick="toggleNotifications()" class="relative p-2.5 rounded-xl bg-slate-900/80 border border-sky-500/20 text-slate-300 hover:text-white hover:border-sky-400 transition-all">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
                    <span id="notif-badge" class="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-lg shadow-rose-500/50">2</span>
                </button>

                <!-- Notification Dropdown Panel -->
                <div id="notif-panel" class="hidden absolute right-0 mt-3 w-80 md:w-96 glass-card p-4 shadow-2xl border-sky-500/30 z-50">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                        <h3 class="font-semibold text-sm text-sky-300 flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> Live Alerts Feed
                        </h3>
                        <button onclick="clearNotifs()" class="text-xs text-slate-400 hover:text-rose-400 transition">Clear All</button>
                    </div>
                    <div id="notif-list" class="mt-3 space-y-2.5 max-h-72 overflow-y-auto pr-1">
                        <!-- Dynamic notification items injected here -->
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Dynamic Content Container -->
    <main class="max-w-7xl mx-auto px-6 pt-8">

        <!-- ================= PAGE 1: HOME & BENTO OVERVIEW ================= -->
        <section id="page-home" class="page-view space-y-8">
            <div class="text-center max-w-3xl mx-auto space-y-3">
                <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-semibold tracking-wide">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> SDG 3 HEALTH & WELLBEING
                </span>
                <h1 class="text-4xl md:text-5xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-200 to-indigo-300">
                    Next-Gen Precision Patient Companion
                </h1>
                <p class="text-slate-400 text-sm md:text-base">
                    Smart disease triage, multi-week adherence tracking, family caregiver sync, and one-tap emergency response built for low-resource scalability.
                </p>
            </div>

            <!-- Bento Stats Header -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass-card p-6 flex items-center gap-4">
                    <div class="p-4 rounded-2xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
                        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </div>
                    <div>
                        <p class="text-xs font-medium text-slate-400">Treatment Plan Status</p>
                        <h3 class="text-xl font-bold text-white">Week 1 Active</h3>
                        <p class="text-xs text-emerald-400 font-semibold mt-0.5">↑ 92% Adherence Rate</p>
                    </div>
                </div>

                <div class="glass-card p-6 flex items-center gap-4">
                    <div class="p-4 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    </div>
                    <div>
                        <p class="text-xs font-medium text-slate-400">Emergency GPS</p>
                        <h3 class="text-xl font-bold text-white">Live Tracking</h3>
                        <p class="text-xs text-sky-400 font-semibold mt-0.5">Kolhapur Central Node</p>
                    </div>
                </div>

                <div class="glass-card p-6 flex items-center gap-4">
                    <div class="p-4 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                    </div>
                    <div>
                        <p class="text-xs font-medium text-slate-400">Caregiver Portal</p>
                        <h3 class="text-xl font-bold text-white">Synced 🔒</h3>
                        <p class="text-xs text-indigo-400 font-semibold mt-0.5">PIN Access Enabled</p>
                    </div>
                </div>
            </div>

            <!-- Bento Quick Action Tiles -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass-card p-6 space-y-4 hover:border-sky-400/50 cursor-pointer" onclick="switchPage('hospital')">
                    <div class="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Hospital Finder & Map</h3>
                    <p class="text-sm text-slate-400">Intelligent disease-to-hospital routing with interactive canvas map pinpoints.</p>
                    <span class="inline-flex items-center gap-1 text-xs font-semibold text-sky-400">Launch Finder →</span>
                </div>

                <div class="glass-card p-6 space-y-4 hover:border-indigo-400/50 cursor-pointer" onclick="switchPage('hospital')">
                    <div class="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Medication Schedule</h3>
                    <p class="text-sm text-slate-400">Multi-week treatment logs (Weeks 1-4) with automated categorization & tracking.</p>
                    <span class="inline-flex items-center gap-1 text-xs font-semibold text-indigo-400">View Schedule →</span>
                </div>

                <div class="glass-card p-6 space-y-4 hover:border-rose-400/50 cursor-pointer" onclick="switchPage('passport')">
                    <div class="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Medical Passport & SOS</h3>
                    <p class="text-sm text-slate-400">Offline medical passport card and one-tap emergency broadcasting to family.</p>
                    <span class="inline-flex items-center gap-1 text-xs font-semibold text-rose-400">Open Passport →</span>
                </div>
            </div>
        </section>

        <!-- ================= PAGE 2: HOSPITAL FINDER & MEDICATION SUITE ================= -->
        <section id="page-hospital" class="page-view hidden space-y-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-3xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-300 to-indigo-300">
                        Hospital Triage & Medication Suite
                    </h2>
                    <p class="text-slate-400 text-sm">Smart condition search, interactive hospital routing map, and multi-week medication schedule.</p>
                </div>
            </div>

            <!-- Triage Search Input -->
            <div class="glass-card p-6 space-y-4">
                <label class="block text-sm font-semibold text-sky-300">🔍 Search Symptom / Disease Condition:</label>
                <div class="flex flex-col sm:flex-row gap-3">
                    <input type="text" id="disease-search" placeholder="Type condition (e.g., Heart, Eye, Bones/Fracture)..." onkeyup="handleTriageSearch()" class="gooey-input flex-1">
                    <button onclick="handleTriageSearch()" class="magnetic-btn">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Search Facility
                    </button>
                </div>

                <div id="triage-result" class="p-4 rounded-xl bg-slate-900/90 border border-sky-500/20 text-sm">
                    <p class="text-slate-300">📍 Recommended Facility: <strong class="text-white" id="hosp-name">Alliance Multispeciality Hospital</strong> — <span class="text-sky-400" id="hosp-dist">~2.1 km away | 5 mins via City Road</span></p>
                </div>
            </div>

            <!-- Interactive Canvas Hospital Map -->
            <div class="glass-card p-6 space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold text-white flex items-center gap-2">
                        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
                        Interactive Specialized Route Map
                    </h3>
                    <span class="text-xs text-slate-400">Cyan Pin = GPS Location | Rose Pin = Hospital</span>
                </div>
                <div class="relative w-full h-72 rounded-2xl overflow-hidden border border-slate-800 bg-slate-950">
                    <canvas id="map-canvas" class="w-full h-full"></canvas>
                </div>
            </div>

            <!-- Multi-Week Medication Schedule & Doctor Questions Split -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Schedule Module -->
                <div class="glass-card p-6 space-y-5">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-bold text-white flex items-center gap-2">
                            <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg> Multi-Week Medication Schedule
                        </h3>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Select Week:</label>
                            <select id="week-select" onchange="renderMedications()" class="gooey-input w-full text-sm">
                                <option value="Week 1">Week 1</option>
                                <option value="Week 2">Week 2</option>
                                <option value="Week 3">Week 3</option>
                                <option value="Week 4">Week 4</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Select Day:</label>
                            <select id="day-select" onchange="renderMedications()" class="gooey-input w-full text-sm">
                                <option value="Monday">Monday</option>
                                <option value="Tuesday">Tuesday</option>
                                <option value="Wednesday">Wednesday</option>
                                <option value="Thursday">Thursday</option>
                                <option value="Friday">Friday</option>
                                <option value="Saturday">Saturday</option>
                                <option value="Sunday">Sunday</option>
                            </select>
                        </div>
                    </div>

                    <!-- Medication Items Container -->
                    <div id="med-list" class="space-y-3 pt-2">
                        <!-- Dynamic meds injected here -->
                    </div>
                </div>

                <!-- Doctor Appointments & Questions -->
                <div class="glass-card p-6 space-y-5">
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Doctor Appointment Notes
                    </h3>

                    <div class="p-4 rounded-xl bg-slate-900/80 border border-sky-500/20 space-y-1">
                        <p class="text-sm font-semibold text-white">Dr. Sharma (Cardiologist)</p>
                        <p class="text-xs text-sky-400">📅 Tomorrow at 10:30 AM | City General Hospital</p>
                    </div>

                    <div class="space-y-3">
                        <label class="block text-xs text-slate-300">Add Question for Doctor:</label>
                        <div class="flex gap-2">
                            <input type="text" id="doc-q-input" placeholder="e.g. Any dietary restrictions with dosage?" class="gooey-input flex-1 text-sm">
                            <button onclick="addQuestion()" class="magnetic-btn text-sm">Add</button>
                        </div>
                    </div>

                    <div class="space-y-2">
                        <p class="text-xs font-semibold text-slate-400">Saved Questions:</p>
                        <ul id="q-list" class="space-y-2 text-xs text-slate-300 max-h-40 overflow-y-auto pr-1">
                            <!-- Questions injected here -->
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= PAGE 3: CAREGIVER LIVE SYNC ================= -->
        <section id="page-caregiver" class="page-view hidden space-y-8">
            <div class="max-w-3xl mx-auto space-y-6">
                <div>
                    <h2 class="text-3xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-300 to-indigo-300">
                        Caregiver Prescription Portal
                    </h2>
                    <p class="text-slate-400 text-sm">Remote patient monitoring, prescription creation, and live push alert dispatching.</p>
                </div>

                <!-- PIN Authorization Card -->
                <div id="pin-card" class="glass-card p-6 space-y-4">
                    <label class="block text-sm font-semibold text-sky-300">🔒 Enter Caregiver Access PIN:</label>
                    <div class="flex gap-3">
                        <input type="password" id="caregiver-pin" placeholder="Enter PIN (Demo PIN: 1234)" class="gooey-input flex-1">
                        <button onclick="unlockCaregiver()" class="magnetic-btn">Unlock Portal</button>
                    </div>
                    <p id="pin-msg" class="text-xs text-slate-400">Default Demo PIN is <code class="text-sky-400 font-bold">1234</code></p>
                </div>

                <!-- Unlocked Caregiver Controls -->
                <div id="caregiver-content" class="hidden space-y-6">
                    <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm flex items-center justify-between">
                        <span>🔓 Authorized Caregiver: Linked to Patient #PAT-8821</span>
                        <button onclick="lockCaregiver()" class="text-xs text-slate-400 hover:text-white underline">Lock Session</button>
                    </div>

                    <!-- Assign New Medication Form -->
                    <div class="glass-card p-6 space-y-4">
                        <h3 class="text-lg font-bold text-white flex items-center gap-2">
                            <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg> Assign New Prescription
                        </h3>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs text-slate-400 mb-1">Medicine Name & Dosage:</label>
                                <input type="text" id="new-med-name" placeholder="e.g. Paracetamol (650mg)" class="gooey-input w-full text-sm">
                            </div>
                            <div>
                                <label class="block text-xs text-slate-400 mb-1">Scheduled Time:</label>
                                <input type="text" id="new-med-time" placeholder="e.g. 02:00 PM" class="gooey-input w-full text-sm">
                            </div>
                            <div>
                                <label class="block text-xs text-slate-400 mb-1">Assign Week:</label>
                                <select id="new-med-week" class="gooey-input w-full text-sm">
                                    <option value="All Weeks">All Weeks (Weeks 1-4)</option>
                                    <option value="Week 1">Week 1 Only</option>
                                    <option value="Week 2">Week 2 Only</option>
                                    <option value="Week 3">Week 3 Only</option>
                                    <option value="Week 4">Week 4 Only</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs text-slate-400 mb-1">Assign Day:</label>
                                <select id="new-med-day" class="gooey-input w-full text-sm">
                                    <option value="All Days">All Days (Mon-Sun)</option>
                                    <option value="Monday">Monday</option>
                                    <option value="Tuesday">Tuesday</option>
                                    <option value="Wednesday">Wednesday</option>
                                    <option value="Thursday">Thursday</option>
                                    <option value="Friday">Friday</option>
                                    <option value="Saturday">Saturday</option>
                                    <option value="Sunday">Sunday</option>
                                </select>
                            </div>
                        </div>

                        <button onclick="addCaregiverMed()" class="magnetic-btn w-full justify-center">
                            Save & Dispatch Prescription
                        </button>
                    </div>

                    <!-- Send Push Notification Note -->
                    <div class="glass-card p-6 space-y-4">
                        <h3 class="text-lg font-bold text-white flex items-center gap-2">
                            <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c.41 0 .824-.102 1.201-.295l2.454-1.256A2 2 0 0115.34 6v12a2 2 0 01-2.853 1.83l-2.454-1.256a1.998 1.998 0 00-1.2-.295H7a4.001 4.001 0 01-1.564-.317z"/></svg> Dispatch Patient Encouragement Note
                        </h3>
                        <textarea id="push-note" rows="2" placeholder="Send an encouraging message or alert..." class="gooey-input w-full text-sm"></textarea>
                        <button onclick="sendCaregiverPush()" class="magnetic-btn w-full justify-center">
                            Send Push Notification
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= PAGE 4: DIGITAL MEDICAL PASSPORT & SOS ================= -->
        <section id="page-passport" class="page-view hidden space-y-8">
            <div class="max-w-4xl mx-auto space-y-6">
                <div>
                    <h2 class="text-3xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-300 to-indigo-300">
                        Secure Medical Passport & Emergency SOS
                    </h2>
                    <p class="text-slate-400 text-sm">Offline medical credentials and instant high-priority emergency broadcast.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Passport ID Card -->
                    <div class="glass-card p-6 space-y-4 relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-32 h-32 bg-sky-500/10 rounded-full blur-2xl pointer-events-none"></div>
                        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                            <span class="text-xs font-bold tracking-wider text-sky-400 uppercase">Emergency Medical ID</span>
                            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-400">ACTIVE</span>
                        </div>

                        <div class="space-y-2 text-sm text-slate-300">
                            <p class="flex justify-between"><span class="text-slate-500">Full Name:</span> <strong class="text-white">Manas S. Abitkar</strong></p>
                            <p class="flex justify-between"><span class="text-slate-500">Blood Group:</span> <strong class="text-rose-400 font-bold">O+ Positive</strong></p>
                            <p class="flex justify-between"><span class="text-slate-500">Primary Caregiver:</span> <strong class="text-white">+91 98765 43210</strong></p>
                            <p class="flex justify-between"><span class="text-slate-500">Known Allergies:</span> <strong class="text-amber-400">Penicillin, Peanuts</strong></p>
                            <p class="flex justify-between"><span class="text-slate-500">Conditions:</span> <strong class="text-sky-300">Type 2 Diabetes, BP</strong></p>
                            <p class="flex justify-between"><span class="text-slate-500">Primary Physician:</span> <strong class="text-white">Dr. Sharma (City Hospital)</strong></p>
                        </div>

                        <button onclick="downloadID()" class="magnetic-btn w-full justify-center text-sm py-2.5 mt-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg> Download Secure ID Pass
                        </button>
                    </div>

                    <!-- One-Tap Emergency SOS Trigger -->
                    <div class="glass-card p-6 space-y-4 border-rose-500/30">
                        <div class="flex items-center gap-2 text-rose-400 font-bold text-lg">
                            <svg class="w-6 h-6 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                            Emergency SOS Broadcast
                        </div>

                        <p class="text-xs text-slate-300 leading-relaxed">
                            Pressing this button broadcasts your live GPS coordinates to linked emergency services and caregiver notification logs immediately.
                        </p>

                        <textarea id="sos-msg" rows="2" placeholder="Optional SOS Note (e.g., Experiencing severe dizziness)..." class="gooey-input w-full text-sm border-rose-500/30 focus:border-rose-500"></textarea>

                        <button onclick="triggerSOS()" class="w-full py-4 rounded-2xl bg-gradient-to-r from-rose-600 via-red-500 to-rose-700 text-white font-bold text-base shadow-xl shadow-rose-600/50 hover:shadow-rose-600/80 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
                            TRIGGER EMERGENCY SOS
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= PAGE 5: SDG 3 IMPACT & METRICS ================= -->
        <section id="page-impact" class="page-view hidden space-y-8">
            <div class="max-w-4xl mx-auto space-y-6">
                <div>
                    <h2 class="text-3xl font-serif font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-300 to-indigo-300">
                        UN Sustainable Development Goal 3 Impact
                    </h2>
                    <p class="text-slate-400 text-sm">Quantifiable healthcare outcomes for universal health coverage & well-being.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="glass-card p-6 space-y-3">
                        <span class="text-4xl font-bold text-sky-400">38%</span>
                        <h3 class="text-lg font-bold text-white">Reduction in Missed Doses</h3>
                        <p class="text-sm text-slate-400">Achieved via proactive multi-week schedule automation and family caregiver synchronization.</p>
                    </div>

                    <div class="glass-card p-6 space-y-3">
                        <span class="text-4xl font-bold text-emerald-400">45%</span>
                        <h3 class="text-lg font-bold text-white">Emergency Triage Time Saved</h3>
                        <p class="text-sm text-slate-400">Facilitated by direct condition-to-specialty facility routing and live GPS broadcast.</p>
                    </div>
                </div>

                <div class="glass-card p-6 space-y-3 border-sky-500/30">
                    <h3 class="text-xl font-bold text-white flex items-center gap-2">
                        <svg class="w-6 h-6 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 002 2h1.5a2.5 2.5 0 002.5-2.5V11a2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064"/></svg> Low-Resource Rural Scalability
                    </h3>
                    <p class="text-sm text-slate-300 leading-relaxed">
                        HealthBridge operates efficiently in low-bandwidth rural environments, ensuring digital medical passports and basic medication logs stay functional even in offline mode.
                    </p>
                </div>
            </div>
        </section>

    </main>

    <!-- Apple-Style Floating Navigation Dock -->
    <nav class="dock-container">
        <button onclick="switchPage('home')" id="dock-home" class="dock-btn active">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="dock-tooltip">Home Overview</span>
        </button>

        <button onclick="switchPage('hospital')" id="dock-hospital" class="dock-btn">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            <span class="dock-tooltip">Hospital & Meds</span>
        </button>

        <button onclick="switchPage('caregiver')" id="dock-caregiver" class="dock-btn">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            <span class="dock-tooltip">Caregiver Sync</span>
        </button>

        <button onclick="switchPage('passport')" id="dock-passport" class="dock-btn">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
            <span class="dock-tooltip">Medical Passport & SOS</span>
        </button>

        <button onclick="switchPage('impact')" id="dock-impact" class="dock-btn">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 002 2h1.5a2.5 2.5 0 002.5-2.5V11a2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064"/></svg>
            <span class="dock-tooltip">SDG 3 Impact</span>
        </button>
    </nav>

    <!-- Application JavaScript Logic -->
    <script>
        // --- 1. GLOBAL STATE MANAGEMENT ---
        const state = {
            notifications: [
                { msg: "System initialization complete. Connected to Kolhapur GPS.", time: "10 mins ago" },
                { msg: "Caregiver assigned new medication schedule.", time: "1 hour ago" }
            ],
            questions: [
                "Are there any specific dietary restrictions with this dosage?"
            ],
            medications: {
                "Week 1": {
                    "Monday": [
                        { name: "Metformin (500mg)", time: "08:00 AM", category: "Diabetes", taken: false },
                        { name: "Amlodipine (5mg)", time: "01:00 PM", category: "Blood Pressure", taken: true }
                    ],
                    "Tuesday": [
                        { name: "Vitamin D3", time: "08:00 PM", category: "Wellness", taken: false }
                    ]
                },
                "Week 2": {}, "Week 3": {}, "Week 4": {}
            },
            currentMapPin: { name: "Alliance Multispeciality Hospital", type: "General" }
        };

        // Initialize empty days across weeks
        const weeks = ["Week 1", "Week 2", "Week 3", "Week 4"];
        const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        weeks.forEach(w => {
            if (!state.medications[w]) state.medications[w] = {};
            days.forEach(d => {
                if (!state.medications[w][d]) state.medications[w][d] = [];
            });
        });

        // --- 2. SINGLE PAGE APPLICATION ROUTER ---
        function switchPage(pageId) {
            // Hide all pages
            document.querySelectorAll('.page-view').forEach(el => el.classList.add('hidden'));
            
            // Show target page
            const targetPage = document.getElementById(`page-${pageId}`);
            if (targetPage) targetPage.classList.remove('hidden');

            // Update Dock Active States
            document.querySelectorAll('.dock-btn').forEach(btn => btn.classList.remove('active'));
            const activeDock = document.getElementById(`dock-${pageId}`);
            if (activeDock) activeDock.classList.add('active');

            // Scroll top
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // Trigger Map Resize if Hospital Page opened
            if (pageId === 'hospital') {
                setTimeout(drawMap, 100);
            }
        }

        // --- 3. NOTIFICATION SYSTEM ---
        function renderNotifications() {
            const list = document.getElementById('notif-list');
            const badge = document.getElementById('notif-badge');
            
            badge.innerText = state.notifications.length;
            if (state.notifications.length === 0) {
                badge.classList.add('hidden');
                list.innerHTML = `<p class="text-xs text-slate-500 py-2 text-center">No active notifications</p>`;
                return;
            } else {
                badge.classList.remove('hidden');
            }

            list.innerHTML = state.notifications.map(n => `
                <div class="p-2.5 rounded-lg bg-slate-900/90 border border-sky-500/10 text-xs">
                    <p class="text-slate-200 font-medium">${n.msg}</p>
                    <span class="text-[10px] text-sky-400 mt-1 block">${n.time}</span>
                </div>
            `).join('');
        }

        function toggleNotifications() {
            const panel = document.getElementById('notif-panel');
            panel.classList.toggle('hidden');
        }

        function clearNotifs() {
            state.notifications = [];
            renderNotifications();
        }

        // --- 4. TRIAGE & CANVAS MAP RENDERER ---
        function handleTriageSearch() {
            const input = document.getElementById('disease-search').value.toLowerCase().trim();
            const hospName = document.getElementById('hosp-name');
            const hospDist = document.getElementById('hosp-dist');

            if (input.includes('heart') || input.includes('bp') || input.includes('cardio')) {
                hospName.innerText = "Aster Aadhar Hospital (Cardiology Center)";
                hospDist.innerText = "~3.2 km away | 8 mins via NH48";
                state.currentMapPin = { name: hospName.innerText, type: "Cardiology" };
            } else if (input.includes('eye') || input.includes('vision') || input.includes('blur')) {
                hospName.innerText = "Nandadeep Eye Hospital (Ophthalmology)";
                hospDist.innerText = "~4.5 km away | 12 mins via Tarabai Park";
                state.currentMapPin = { name: hospName.innerText, type: "Eye" };
            } else if (input.includes('bone') || input.includes('fracture') || input.includes('ortho')) {
                hospName.innerText = "Dr. Lande Fracture Hospital (Trauma Center)";
                hospDist.innerText = "~6.0 km away | 15 mins via Main Road";
                state.currentMapPin = { name: hospName.innerText, type: "Orthopedics" };
            } else {
                hospName.innerText = "Alliance Multispeciality Hospital";
                hospDist.innerText = "~2.1 km away | 5 mins via City Road";
                state.currentMapPin = { name: hospName.innerText, type: "General" };
            }

            drawMap();
        }

        function drawMap() {
            const canvas = document.getElementById('map-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;

            const w = canvas.width;
            const h = canvas.height;

            // Clear Background
            ctx.fillStyle = '#020617';
            ctx.fillRect(0, 0, w, h);

            // Draw Grid Lines
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
            ctx.lineWidth = 1;
            for (let x = 0; x < w; x += 30) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
            }
            for (let y = 0; y < h; y += 30) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
            }

            // Route Line
            const p1 = { x: w * 0.25, y: h * 0.6 };
            const p2 = { x: w * 0.75, y: h * 0.35 };

            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 3;
            ctx.setLineDash([6, 6]);
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
            ctx.setLineDash([]);

            // Cyan Pin (User)
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath(); ctx.arc(p1.x, p1.y, 8, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = 'white';
            ctx.font = '10px Plus Jakarta Sans';
            ctx.fillText('You (GPS)', p1.x - 22, p1.y + 20);

            // Rose Pin (Hospital)
            ctx.fillStyle = '#f43f5e';
            ctx.beginPath(); ctx.arc(p2.x, p2.y, 10, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#f8fafc';
            ctx.fillText(state.currentMapPin.name, p2.x - 50, p2.y - 16);
        }

        // --- 5. MEDICATION SCHEDULE LOGIC ---
        function renderMedications() {
            const week = document.getElementById('week-select').value;
            const day = document.getElementById('day-select').value;
            const container = document.getElementById('med-list');

            const list = (state.medications[week] && state.medications[week][day]) || [];

            if (list.length === 0) {
                container.innerHTML = `<p class="text-xs text-slate-500 py-4 text-center">No medications scheduled for ${day} (${week}).</p>`;
                return;
            }

            container.innerHTML = list.map((m, idx) => `
                <div class="p-3 rounded-xl bg-slate-900/80 border border-sky-500/20 flex items-center justify-between text-xs">
                    <div>
                        <p class="font-bold text-white text-sm">${m.name}</p>
                        <p class="text-slate-400">Time: <span class="text-sky-300">${m.time}</span> | Category: <span class="text-indigo-300">${m.category}</span></p>
                    </div>
                    <button onclick="toggleMedState('${week}', '${day}', ${idx})" class="${m.taken ? 'px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-semibold' : 'magnetic-btn py-1 px-3 text-xs'}">
                        ${m.taken ? 'Taken ✓' : 'Mark Taken'}
                    </button>
                </div>
            `).join('');
        }

        function toggleMedState(w, d, idx) {
            state.medications[w][d][idx].taken = !state.medications[w][d][idx].taken;
            renderMedications();
        }

        // --- 6. DOCTOR QUESTIONS LOGIC ---
        function addQuestion() {
            const input = document.getElementById('doc-q-input');
            if (input.value.trim()) {
                state.questions.push(input.value.trim());
                input.value = '';
                renderQuestions();
            }
        }

        function renderQuestions() {
            const list = document.getElementById('q-list');
            list.innerHTML = state.questions.map(q => `
                <li class="flex items-center gap-2 p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                    <span class="text-sky-400">•</span> ${q}
                </li>
            `).join('');
        }

        // --- 7. CAREGIVER PORTAL LOGIC ---
        function unlockCaregiver() {
            const pin = document.getElementById('caregiver-pin').value;
            const msg = document.getElementById('pin-msg');
            if (pin === '1234') {
                document.getElementById('pin-card').classList.add('hidden');
                document.getElementById('caregiver-content').classList.remove('hidden');
            } else {
                msg.innerText = "❌ Incorrect PIN! Try 1234.";
                msg.classList.add('text-rose-400');
            }
        }

        function lockCaregiver() {
            document.getElementById('pin-card').classList.remove('hidden');
            document.getElementById('caregiver-content').classList.add('hidden');
            document.getElementById('caregiver-pin').value = '';
        }

        function addCaregiverMed() {
            const name = document.getElementById('new-med-name').value;
            const time = document.getElementById('new-med-time').value;
            const weekChoice = document.getElementById('new-med-week').value;
            const dayChoice = document.getElementById('new-med-day').value;

            if (!name || !time) {
                alert("Please fill in both Medicine Name and Time!");
                return;
            }

            const targetWeeks = weekChoice === "All Weeks" ? weeks : [weekChoice];
            const targetDays = dayChoice === "All Days" ? days : [dayChoice];

            targetWeeks.forEach(w => {
                targetDays.forEach(d => {
                    state.medications[w][d].push({
                        name: name,
                        time: time,
                        category: name.toLowerCase().includes('bp') ? 'Blood Pressure' : 'General',
                        taken: false
                    });
                });
            });

            state.notifications.unshift({ msg: `New prescription added by caregiver: ${name}`, time: "Just now" });
            renderNotifications();
            renderMedications();
            alert("Prescription assigned & synced successfully!");

            document.getElementById('new-med-name').value = '';
            document.getElementById('new-med-time').value = '';
        }

        function sendCaregiverPush() {
            const text = document.getElementById('push-note').value;
            if (text.trim()) {
                state.notifications.unshift({ msg: `Caregiver Note: ${text.trim()}`, time: "Just now" });
                renderNotifications();
                document.getElementById('push-note').value = '';
                alert("Encouragement note sent to Patient Bell Feed!");
            }
        }

        // --- 8. EMERGENCY SOS BROADCAST ---
        function triggerSOS() {
            const note = document.getElementById('sos-msg').value;
            state.notifications.unshift({
                msg: `🚨 EMERGENCY SOS BROADCAST: Live GPS Sent! ${note ? 'Note: ' + note : ''}`,
                time: "CRITICAL NOW"
            });
            renderNotifications();
            alert("🚨 EMERGENCY SOS BROADCAST SENT TO CAREGIVER & LOCAL EMERGENCY SERVICES!");
        }

        function downloadID() {
            alert("🔒 Secure Medical Passport QR Pass downloaded successfully!");
        }

        // --- 9. CANVAS CLOUD SHADER BACKGROUND ---
        function initCloudCanvas() {
            const canvas = document.getElementById('cloud-canvas');
            const ctx = canvas.getContext('2d');

            let width = canvas.width = window.innerWidth;
            let height = canvas.height = window.innerHeight;

            window.addEventListener('resize', () => {
                width = canvas.width = window.innerWidth;
                height = canvas.height = window.innerHeight;
            });

            const particles = [];
            for (let i = 0; i < 25; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    radius: Math.random() * 180 + 100,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    color: i % 2 === 0 ? 'rgba(56, 189, 248, 0.06)' : 'rgba(129, 140, 248, 0.05)'
                });
            }

            function animate() {
                ctx.clearRect(0, 0, width, height);

                particles.forEach(p => {
                    p.x += p.vx;
                    p.y += p.vy;

                    if (p.x < -p.radius) p.x = width + p.radius;
                    if (p.x > width + p.radius) p.x = -p.radius;
                    if (p.y < -p.radius) p.y = height + p.radius;
                    if (p.y > height + p.radius) p.y = -p.radius;

                    const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius);
                    grad.addColorStop(0, p.color);
                    grad.addColorStop(1, 'rgba(2, 6, 23, 0)');

                    ctx.fillStyle = grad;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fill();
                });

                requestAnimationFrame(animate);
            }

            animate();
        }

        // Window Init
        window.onload = function() {
            initCloudCanvas();
            renderNotifications();
            renderQuestions();
            renderMedications();
            drawMap();
        };
    </script>
</body>
</html>
