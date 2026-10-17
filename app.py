import React, { useState, useEffect, useRef } from 'react';
import { 
  Home, 
  Hospital, 
  Heart, 
  ShieldAlert, 
  Globe, 
  MapPin, 
  Clock, 
  Bell, 
  UserCheck, 
  Plus, 
  Check, 
  Activity, 
  Download, 
  Search, 
  Calendar, 
  ChevronRight,
  AlertTriangle,
  FileText,
  Lock,
  Pill,
  MessageSquare,
  Code,
  FolderTree,
  Terminal
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [notifications, setNotifications] = useState([
    { id: 1, msg: "GitHub Repository Bundle Loaded Successfully", time: "Just now", type: "info" },
    { id: 2, msg: "Cardiology appointment confirmed for tomorrow", time: "10m ago", type: "success" }
  ]);
  const [showNotifications, setShowNotifications] = useState(false);

  const dockItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'hospital', label: 'Hospital Hub', icon: Hospital },
    { id: 'caregiver', label: 'Caregiver Portal', icon: Heart },
    { id: 'passport', label: 'Medical Passport', icon: ShieldAlert },
    { id: 'sdg', label: 'SDG 3 Disease Globe', icon: Globe },
    { id: 'repo', label: 'GitHub Repository Structure', icon: FolderTree }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-sky-500 selection:text-white relative overflow-x-hidden">
      {/* Background Cloud & Atmospheric Glow Animations */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-sky-500/20 rounded-full filter blur-[120px] animate-pulse" />
        <div className="absolute bottom-1/3 right-1/4 w-[30rem] h-[30rem] bg-indigo-500/15 rounded-full filter blur-[140px] animate-pulse" style={{ animationDuration: '8s' }} />
        <div className="absolute top-2/3 left-1/3 w-80 h-80 bg-purple-500/15 rounded-full filter blur-[100px] animate-pulse" style={{ animationDuration: '6s' }} />
      </div>

      {/* Top Header Controls */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/60 border-b border-slate-800/60 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-400 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-white via-sky-200 to-indigo-300 bg-clip-text text-transparent">
              HealthBridge
            </h1>
            <p className="text-xs text-sky-400/80 font-medium">Next.js & Aceternity UI Production Architecture</p>
          </div>
        </div>

        {/* Notifications Popover */}
        <div className="relative">
          <button 
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-sky-500/50 text-slate-300 hover:text-white transition-all relative"
          >
            <Bell className="w-5 h-5" />
            {notifications.length > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-rose-500 text-white rounded-full text-xs flex items-center justify-center font-bold animate-bounce">
                {notifications.length}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-3 w-80 sm:w-96 bg-slate-900/95 border border-sky-500/30 rounded-2xl shadow-2xl backdrop-blur-2xl p-4 z-50">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="font-semibold text-slate-200 flex items-center gap-2">
                  <Bell className="w-4 h-4 text-sky-400" /> Notifications Feed
                </h3>
                <span className="text-xs bg-sky-500/20 text-sky-300 px-2 py-0.5 rounded-full">
                  {notifications.length} New
                </span>
              </div>
              <div className="mt-3 space-y-2 max-h-64 overflow-y-auto pr-1">
                {notifications.map((n) => (
                  <div key={n.id} className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-600 transition-all text-xs">
                    <p className="text-slate-200 font-medium">{n.msg}</p>
                    <span className="text-slate-400 mt-1 block text-[10px]">{n.time}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Instant Main Content Render Engine */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-8 pb-32">
        {activeTab === 'home' && <HomeView setActiveTab={setActiveTab} />}
        {activeTab === 'hospital' && <HospitalHubView />}
        {activeTab === 'caregiver' && <CaregiverPortalView setNotifications={setNotifications} />}
        {activeTab === 'passport' && <MedicalPassportView setNotifications={setNotifications} />}
        {activeTab === 'sdg' && <SDGImpactView />}
        {activeTab === 'repo' && <GitHubRepoStructureView />}
      </main>

      {/* Aceternity Glass Floating Dock */}
      <nav className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
        <div className="flex items-center gap-2 sm:gap-3 bg-slate-900/80 backdrop-blur-2xl border border-sky-500/30 px-4 py-2.5 rounded-full shadow-[0_20px_50px_rgba(0,0,0,0.8)] shadow-sky-950/50">
          {dockItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`group relative p-3 rounded-full transition-all duration-300 ease-out flex items-center justify-center ${
                  isActive 
                    ? 'bg-gradient-to-tr from-sky-500 to-indigo-600 text-white scale-110 shadow-lg shadow-sky-500/40 border border-white/30' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/80 hover:scale-110'
                }`}
              >
                <Icon className="w-5 h-5 sm:w-6 sm:h-6" />
                
                {/* Hover Tooltip */}
                <span className="absolute -top-11 left-1/2 -translate-x-1/2 px-3 py-1 bg-slate-900 border border-sky-500/40 text-slate-200 text-xs font-semibold rounded-lg opacity-0 pointer-events-none group-hover:opacity-100 group-hover:-translate-y-1 transition-all duration-200 whitespace-nowrap shadow-xl">
                  {item.label}
                </span>
              </button>
            );
          })}
        </div>
      </nav>
    </div>
  );
}

// ----------------------------------------------------
// HOME TAB COMPONENT
// ----------------------------------------------------
function HomeView({ setActiveTab }) {
  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Hero Section */}
      <div className="relative rounded-3xl p-8 sm:p-12 overflow-hidden bg-gradient-to-br from-slate-900/90 via-slate-900/60 to-slate-950/90 border border-slate-800 backdrop-blur-2xl shadow-2xl">
        <div className="max-w-2xl space-y-4">
          <span className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-semibold">
            <Activity className="w-3.5 h-3.5" /> Next-Gen SDG 3 Production Companion
          </span>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Precision Healthcare <br />
            <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
              Zero-Delay Triage Architecture
            </span>
          </h1>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Connecting medical triage, offline emergency passports, family prescription sync, and global health impact telemetry in real time. Ready for GitHub deployment.
          </p>
          <div className="flex flex-wrap gap-4 pt-2">
            <button 
              onClick={() => setActiveTab('sdg')}
              className="px-6 py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold shadow-lg shadow-sky-500/25 hover:shadow-sky-500/40 hover:scale-[1.02] transition-all flex items-center gap-2"
            >
              <Globe className="w-4 h-4" /> Explore Disease Globe
            </button>
            <button 
              onClick={() => setActiveTab('repo')}
              className="px-6 py-3 rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-slate-200 font-semibold hover:scale-[1.02] transition-all flex items-center gap-2"
            >
              <FolderTree className="w-4 h-4 text-sky-400" /> View GitHub Repo Code
            </button>
          </div>
        </div>
      </div>

      {/* Quick Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl">
          <p className="text-slate-400 text-xs font-medium">Active Treatment Plan</p>
          <h3 className="text-2xl font-bold text-white mt-1">Week 1 Active</h3>
          <span className="text-xs text-emerald-400 font-semibold inline-block mt-2">↑ 92% Dose Adherence</span>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl">
          <p className="text-slate-400 text-xs font-medium">Emergency Readiness</p>
          <h3 className="text-2xl font-bold text-white mt-1">GPS Active</h3>
          <span className="text-xs text-sky-400 font-semibold inline-block mt-2">Kolhapur Triage Network</span>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl">
          <p className="text-slate-400 text-xs font-medium">Caregiver Sync</p>
          <h3 className="text-2xl font-bold text-white mt-1">Connected 🔒</h3>
          <span className="text-xs text-indigo-400 font-semibold inline-block mt-2">PIN Protected Sync</span>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// HOSPITAL HUB TAB COMPONENT
// ----------------------------------------------------
function HospitalHubView() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedWeek, setSelectedWeek] = useState('Week 1');
  const [selectedDay, setSelectedDay] = useState('Monday');
  const [questions, setQuestions] = useState(["Are there food restrictions with this medication?"]);
  const [newQuestion, setNewQuestion] = useState('');

  const hospitals = [
    { name: "Alliance Multispecialty Hospital", spec: "General & Emergency Triage", lat: "16.6900 N", lon: "74.2200 E", dist: "~2.1 km | 5 mins", key: "general" },
    { name: "Aster Aadhar Hospital (Cardiology Center)", spec: "Cardiology & Cardiac ICU", lat: "16.7050 N", lon: "74.2433 E", dist: "~3.2 km | 8 mins", key: "cardio" },
    { name: "Nandadeep Eye Hospital", spec: "Ophthalmology & Vision Care", lat: "16.7120 N", lon: "74.2500 E", dist: "~4.5 km | 12 mins", key: "eye" },
    { name: "Dr. Lande Fracture Hospital", spec: "Orthopedics & Trauma Unit", lat: "16.7200 N", lon: "74.4600 E", dist: "~6.0 km | 15 mins", key: "ortho" }
  ];

  const filteredHospital = hospitals.find(h => {
    const q = searchTerm.toLowerCase();
    if (q.includes('heart') || q.includes('chest') || q.includes('cardio')) return h.key === 'cardio';
    if (q.includes('eye') || q.includes('vision')) return h.key === 'eye';
    if (q.includes('bone') || q.includes('fracture') || q.includes('ortho')) return h.key === 'ortho';
    return false;
  }) || hospitals[0];

  const handleAddQuestion = (e) => {
    e.preventDefault();
    if (newQuestion.trim()) {
      setQuestions([...questions, newQuestion.trim()]);
      setNewQuestion('');
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <div>
        <h2 className="text-3xl font-bold text-white">Hospital Triage & Schedule Hub</h2>
        <p className="text-slate-400 text-sm mt-1">Symptom-matched facility search and patient appointment management</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-4">
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
            <label className="text-sm font-semibold text-slate-200 block mb-2">Search Condition / Symptom</label>
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3.5 top-3.5 text-slate-400" />
              <input 
                type="text" 
                placeholder="e.g. Heart, Eye, Bone fracture..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700/80 rounded-xl pl-11 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-sky-500 transition-colors"
              />
            </div>

            <div className="mt-6 p-4 rounded-xl bg-sky-950/30 border border-sky-500/30 space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400">Matched Specialty Facility</span>
              <h3 className="text-base font-bold text-white">{filteredHospital.name}</h3>
              <p className="text-xs text-sky-200/80">{filteredHospital.spec}</p>
              <div className="flex items-center gap-2 text-xs text-slate-400 pt-2 border-t border-sky-500/20">
                <MapPin className="w-3.5 h-3.5 text-rose-400" />
                <span>{filteredHospital.dist}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl flex flex-col justify-between relative overflow-hidden min-h-[250px]">
          <div className="absolute inset-0 bg-slate-950 opacity-90" />
          
          <div className="absolute inset-0 flex items-center justify-center opacity-40">
            <svg className="w-full h-full" viewBox="0 0 400 200">
              <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="1" />
              </pattern>
              <rect width="100%" height="100%" fill="url(#grid)" />
              <circle cx="200" cy="100" r="60" fill="none" stroke="#38bdf8" strokeWidth="1" strokeDasharray="4 4" />
            </svg>
          </div>

          <div className="relative z-10 flex justify-between items-start">
            <span className="text-xs bg-slate-800/90 text-slate-300 px-3 py-1 rounded-full border border-slate-700">
              GPS Navigation Telemetry
            </span>
            <span className="text-xs text-emerald-400 font-mono bg-emerald-950/40 border border-emerald-500/30 px-2.5 py-1 rounded-full">
              GPS Signal: Active
            </span>
          </div>

          <div className="relative z-10 my-8 flex items-center justify-around">
            <div className="text-center space-y-1">
              <div className="w-10 h-10 rounded-full bg-sky-500/20 border-2 border-sky-400 flex items-center justify-center mx-auto shadow-lg shadow-sky-500/50 animate-ping">
                <MapPin className="w-5 h-5 text-sky-400" />
              </div>
              <p className="text-xs font-bold text-white">Your Location</p>
              <p className="text-[10px] text-slate-400">Kolhapur Central</p>
            </div>

            <div className="h-0.5 flex-1 bg-gradient-to-r from-sky-500 to-rose-500 mx-4 border-t border-dashed border-sky-300" />

            <div className="text-center space-y-1">
              <div className="w-10 h-10 rounded-full bg-rose-500/20 border-2 border-rose-500 flex items-center justify-center mx-auto shadow-lg shadow-rose-500/50">
                <Hospital className="w-5 h-5 text-rose-400" />
              </div>
              <p className="text-xs font-bold text-white">{filteredHospital.name.split(' ')[0]}</p>
              <p className="text-[10px] text-rose-300">{filteredHospital.spec.split('&')[0]}</p>
            </div>
          </div>

          <div className="relative z-10 flex items-center justify-between text-xs text-slate-400 bg-slate-900/90 p-3 rounded-xl border border-slate-800">
            <span>Latitude: {filteredHospital.lat}</span>
            <span>Longitude: {filteredHospital.lon}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// CAREGIVER PORTAL TAB COMPONENT
// ----------------------------------------------------
function CaregiverPortalView({ setNotifications }) {
  const [pin, setPin] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [medName, setMedName] = useState('');
  const [medTime, setMedTime] = useState('');

  const handleUnlock = (e) => {
    e.preventDefault();
    if (pin === '1234') {
      setIsUnlocked(true);
    } else {
      alert('Demo PIN is 1234');
    }
  };

  const handleAddMedication = (e) => {
    e.preventDefault();
    if (medName && medTime) {
      setNotifications(prev => [
        { id: Date.now(), msg: `Caregiver added ${medName}`, time: "Just now" },
        ...prev
      ]);
      setMedName('');
      setMedTime('');
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <div>
        <h2 className="text-3xl font-bold text-white">Caregiver Portal</h2>
        <p className="text-slate-400 text-sm mt-1">Remote family prescription sync and medication adherence tracking</p>
      </div>

      {!isUnlocked ? (
        <div className="max-w-md mx-auto p-8 rounded-3xl bg-slate-900/90 border border-slate-800 backdrop-blur-2xl text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center mx-auto text-indigo-400">
            <Lock className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Protected Family Portal</h3>
            <p className="text-xs text-slate-400 mt-1">Enter PIN to access patient record (Demo PIN: <span className="text-sky-400 font-mono">1234</span>)</p>
          </div>
          <form onSubmit={handleUnlock} className="space-y-4">
            <input 
              type="password" 
              maxLength={4}
              placeholder="Enter PIN"
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-center text-xl font-mono text-white tracking-widest focus:outline-none focus:border-indigo-500"
            />
            <button type="submit" className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold shadow-lg shadow-indigo-500/30 hover:scale-[1.01] transition-all">
              Unlock Caregiver Portal
            </button>
          </form>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <UserCheck className="w-6 h-6 text-emerald-400" />
              <div>
                <p className="text-sm font-bold text-white">Connected to Patient Profile #PAT-8821</p>
                <p className="text-xs text-slate-300">Remote Synchronization Active</p>
              </div>
            </div>
            <button onClick={() => setIsUnlocked(false)} className="text-xs text-slate-400 hover:text-white underline">
              Lock Session
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// ----------------------------------------------------
// MEDICAL PASSPORT TAB COMPONENT
// ----------------------------------------------------
function MedicalPassportView({ setNotifications }) {
  const [sosActive, setSosActive] = useState(false);

  const handleTriggerSOS = () => {
    setSosActive(true);
    setNotifications(prev => [
      { id: Date.now(), msg: "🚨 CRITICAL EMERGENCY SOS BROADCASTED TO NEARBY TRIAGE CENTERS!", time: "Just now" },
      ...prev
    ]);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <div>
        <h2 className="text-3xl font-bold text-white">Medical ID & Emergency SOS</h2>
        <p className="text-slate-400 text-sm mt-1">Offline medical record QR passport and live triage broadcast</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 backdrop-blur-xl space-y-6 relative overflow-hidden">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-sky-500/20 border border-sky-400/40 flex items-center justify-center font-bold text-sky-400 text-lg">
                MS
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Manas S. Abitkar</h3>
                <p className="text-xs text-slate-400">Passport ID: HB-99201-GLOBAL</p>
              </div>
            </div>
            <span className="px-3 py-1 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30 font-bold text-xs">
              O+ POSITIVE
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <p className="text-slate-400">Emergency Contact</p>
              <p className="font-semibold text-slate-200 mt-0.5">+91 98765 43210</p>
            </div>
            <div>
              <p className="text-slate-400">Primary Physician</p>
              <p className="font-semibold text-slate-200 mt-0.5">Dr. Sharma (Cardiology)</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-3xl bg-slate-900/80 border border-rose-500/30 backdrop-blur-xl space-y-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-rose-400 font-bold text-sm uppercase tracking-wider mb-2">
              <AlertTriangle className="w-4 h-4" /> Emergency Triage Broadcast
            </div>
            <h3 className="text-2xl font-bold text-white">One-Tap SOS Beacon</h3>
            <p className="text-slate-400 text-xs mt-2 leading-relaxed">
              Instantly sends your live GPS location, blood group, and allergy list to nearby emergency responder networks.
            </p>
          </div>

          {sosActive ? (
            <div className="p-4 rounded-2xl bg-rose-950/80 border border-rose-500 text-center space-y-2 animate-pulse">
              <p className="text-rose-200 font-bold text-sm">🚨 EMERGENCY SOS BROADCAST ACTIVE</p>
              <p className="text-xs text-rose-300">Live GPS Coordinates Transmitted to Regional Dispatch</p>
              <button 
                onClick={() => setSosActive(false)}
                className="mt-2 text-xs text-slate-300 hover:text-white underline"
              >
                Cancel Beacon
              </button>
            </div>
          ) : (
            <button 
              onClick={handleTriggerSOS}
              className="w-full py-5 rounded-2xl bg-gradient-to-r from-rose-600 to-red-700 hover:from-rose-500 hover:to-red-600 text-white font-black tracking-wider text-base shadow-xl shadow-rose-600/40 hover:scale-[1.02] transition-all flex items-center justify-center gap-3"
            >
              <ShieldAlert className="w-6 h-6 animate-bounce" /> BROADCAST EMERGENCY SOS
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// SDG 3 IMPACT TAB WITH COUNTRY HIGHEST DISEASE GLOBE
// ----------------------------------------------------
function SDGImpactView() {
  return (
    <div className="space-y-8 animate-fadeIn">
      <div>
        <h2 className="text-3xl font-bold text-white">UN SDG 3 Impact Telemetry</h2>
        <p className="text-slate-400 text-sm mt-1">Interactive 3D canvas rendering highest disease burdens by country</p>
      </div>

      <div className="relative rounded-3xl bg-slate-900/90 border border-slate-800 p-6 backdrop-blur-2xl overflow-hidden min-h-[500px] flex flex-col justify-between">
        <div className="absolute top-6 left-6 z-10 space-y-1">
          <span className="text-xs bg-sky-500/20 text-sky-300 border border-sky-500/30 px-3 py-1 rounded-full font-semibold">
            Global Health Monitor
          </span>
          <h3 className="text-xl font-bold text-white mt-1">Country Highest Disease Burden Map</h3>
          <p className="text-xs text-slate-400">Drag canvas globe to rotate • View primary disease burden per country</p>
        </div>

        <Globe3DCanvas />

        <div className="relative z-10 grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-slate-800">
          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
            <p className="text-[10px] text-slate-400">Target SDG 3.4</p>
            <p className="text-sm font-bold text-sky-400 mt-0.5">Non-Communicable Diseases</p>
            <p className="text-[10px] text-slate-300 mt-1">Cardiovascular & Diabetes Triage</p>
          </div>
          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
            <p className="text-[10px] text-slate-400">Target SDG 3.8</p>
            <p className="text-sm font-bold text-emerald-400 mt-0.5">Universal Health Access</p>
            <p className="text-[10px] text-slate-300 mt-1">Offline Medical Passport Beacon</p>
          </div>
          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
            <p className="text-[10px] text-slate-400">Triage Time Saved</p>
            <p className="text-sm font-bold text-purple-400 mt-0.5">45% Faster Response</p>
            <p className="text-[10px] text-slate-300 mt-1">Real-time specialty mapping</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// 3D Interactive Canvas Globe Component with Country Disease Data
function Globe3DCanvas() {
  const canvasRef = useRef(null);

  // Highest Disease Burden per Country
  const diseaseMarkers = [
    { country: "India", lat: 28.6139, lng: 77.2090, disease: "Ischemic Heart Disease", cases: "3.2M", color: "#f43f5e" },
    { country: "United Kingdom", lat: 51.5074, lng: -0.1278, disease: "Alzheimer's & Dementia", cases: "890K", color: "#38bdf8" },
    { country: "Japan", lat: 35.6762, lng: 139.6503, disease: "Cerebrovascular Stroke", cases: "1.1M", color: "#a855f7" },
    { country: "United States", lat: 40.7128, lng: -74.0060, disease: "Hypertension & Diabetes", cases: "2.4M", color: "#fbbf24" },
    { country: "Australia", lat: -33.8688, lng: 151.2093, disease: "Skin Melanoma", cases: "420K", color: "#34d399" },
    { country: "Brazil", lat: -22.9068, lng: -43.1729, disease: "Dengue & Arbovirus", cases: "1.5M", color: "#f97316" },
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let rotationX = 0.2;
    let rotationY = 0;
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let animationFrameId;

    const resizeCanvas = () => {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = 420;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const handleMouseDown = (e) => {
      isDragging = true;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const handleMouseMove = (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;

      rotationY += deltaX * 0.008;
      rotationX += deltaY * 0.008;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const handleMouseUp = () => { isDragging = false; };

    canvas.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;
      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.min(width, height) * 0.32;

      if (!isDragging) {
        rotationY += 0.003;
      }

      const atmosphereGradient = ctx.createRadialGradient(centerX, centerY, radius * 0.85, centerX, centerY, radius * 1.25);
      atmosphereGradient.addColorStop(0, 'rgba(56, 189, 248, 0.15)');
      atmosphereGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = atmosphereGradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius * 1.25, 0, Math.PI * 2);
      ctx.fill();

      const globeGradient = ctx.createRadialGradient(centerX - radius * 0.3, centerY - radius * 0.3, 10, centerX, centerY, radius);
      globeGradient.addColorStop(0, '#1e293b');
      globeGradient.addColorStop(0.7, '#0f172a');
      globeGradient.addColorStop(1, '#020617');
      ctx.fillStyle = globeGradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      for (let lat = -60; lat <= 60; lat += 30) {
        const phi = (lat * Math.PI) / 180;
        const r = radius * Math.cos(phi);
        const y = centerY + radius * Math.sin(phi) * Math.cos(rotationX);

        ctx.beginPath();
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
        ctx.ellipse(centerX, y, r, r * Math.sin(rotationX), 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      diseaseMarkers.forEach((m) => {
        const phi = (90 - m.lat) * (Math.PI / 180);
        const theta = (m.lng * (Math.PI / 180)) + rotationY;

        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.sin(phi) * Math.sin(theta);
        const z = radius * Math.cos(phi);

        const rotatedY = y * Math.cos(rotationX) - z * Math.sin(rotationX);
        const rotatedZ = y * Math.sin(rotationX) + z * Math.cos(rotationX);

        if (rotatedZ > 0) {
          const projectedX = centerX + x;
          const projectedY = centerY + rotatedY;

          ctx.beginPath();
          ctx.arc(projectedX, projectedY, 6, 0, Math.PI * 2);
          ctx.fillStyle = m.color;
          ctx.shadowColor = m.color;
          ctx.shadowBlur = 12;
          ctx.fill();
          ctx.shadowBlur = 0;

          ctx.font = 'bold 11px sans-serif';
          ctx.fillStyle = '#f8fafc';
          ctx.fillText(`${m.country}: ${m.disease}`, projectedX + 10, projectedY + 4);
        }
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      canvas.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <canvas ref={canvasRef} className="cursor-grab active:cursor-grabbing max-w-full" />
      <div className="absolute bottom-16 left-6 right-6 sm:left-auto sm:right-6 bg-slate-950/90 border border-sky-500/30 p-3 rounded-2xl backdrop-blur-xl flex items-center justify-between gap-4 z-20">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-rose-500 animate-ping" />
          <span className="text-xs text-slate-200 font-semibold">Highest Burden Indicator: Country Level</span>
        </div>
        <span className="text-xs text-sky-400 font-mono">Live Telemetry</span>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// GITHUB REPOSITORY STRUCTURE & CODES VIEW
// ----------------------------------------------------
function GitHubRepoStructureView() {
  return (
    <div className="space-y-8 animate-fadeIn">
      <div>
        <h2 className="text-3xl font-bold text-white flex items-center gap-3">
          <FolderTree className="w-8 h-8 text-sky-400" /> GitHub Repository Architecture
        </h2>
        <p className="text-slate-400 text-sm mt-1">Production Next.js + Aceternity UI deployment bundle structure</p>
      </div>

      {/* Package.json code box */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 text-slate-300">
          <span className="flex items-center gap-2 text-sky-400 font-bold"><Code className="w-4 h-4" /> package.json</span>
          <span className="text-[10px] text-slate-500">Root Directory</span>
        </div>
        <pre className="text-slate-300 overflow-x-auto p-3 bg-slate-950 rounded-xl leading-relaxed">
{`{
  "name": "healthbridge-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0",
    "framer-motion": "^11.0.8",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1"
  }
}`}
        </pre>
      </div>

      {/* Directory Layout Tree */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 text-slate-300">
          <span className="flex items-center gap-2 text-emerald-400 font-bold"><FolderTree className="w-4 h-4" /> Folder Structure</span>
          <span className="text-[10px] text-slate-500">GitHub Ready</span>
        </div>
        <pre className="text-slate-300 overflow-x-auto p-3 bg-slate-950 rounded-xl leading-relaxed">
{`healthbridge/
├── app/
│   ├── layout.tsx         # Global fonts and metadata
│   ├── page.tsx           # Home & Client tab switcher
│   └── globals.css        # Tailwind and dark glow animations
├── components/
│   ├── ui/
│   │   ├── floating-dock.tsx  # Aceternity floating dock
│   │   └── 3d-globe.tsx       # Country highest disease canvas
│   └── views/
│       ├── HospitalHub.tsx
│       ├── CaregiverPortal.tsx
│       └── MedicalPassport.tsx
├── package.json
└── tailwind.config.js`}
        </pre>
      </div>
    </div>
  );
}
