import React, { useState, useEffect } from 'react';
import { X, Copy, Check, Globe } from 'lucide-react';
import { logError } from '@/lib/logger';

interface BrowserAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function BrowserAuthModal({ isOpen, onClose, onSuccess }: BrowserAuthModalProps) {
  const [service, setService] = useState('openai');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [extractionScript, setExtractionScript] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Fetch the extraction script from backend
    fetch('/api/proxy/api/wallet/browser/extraction-script')
      .then(res => res.json())
      .then(data => setExtractionScript(data.script))
      .catch(err => logError("Failed to load script", { error: err instanceof Error ? err.message : 'Unknown error' }));
  }, []);

  const handleCopyScript = () => {
    navigator.clipboard.writeText(extractionScript);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSubmit = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch('/api/proxy/api/wallet/browser/save-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service,
          token,
          user_agent: navigator.userAgent
        })
      });
      
      if (!res.ok) throw new Error('Failed to save token');
      
      onSuccess();
      onClose();
    } catch {
      alert('Failed to save session token');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const getServiceUrl = () => {
    switch(service) {
      case 'openai': return 'https://chat.openai.com';
      case 'anthropic': return 'https://claude.ai';
      case 'google': return 'https://aistudio.google.com';
      default: return 'https://chat.openai.com';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div className="bg-gray-900 border border-emerald-500/50 rounded-lg max-w-2xl w-full shadow-2xl relative">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-white"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="p-6">
          <h2 className="text-xl font-bold text-emerald-400 mb-6 flex items-center">
            <Globe className="w-5 h-5 mr-2" /> Browser Session Bridge
          </h2>

          <div className="space-y-6">
            {/* Service Selection */}
            <div>
              <label className="block text-xs uppercase text-gray-500 mb-2">1. Select Service</label>
              <select 
                value={service} 
                onChange={(e) => setService(e.target.value)}
                className="w-full bg-black border border-gray-700 rounded p-2 text-white"
                aria-label="Select Service"
              >
                <option value="openai">OpenAI (ChatGPT)</option>
                <option value="anthropic">Anthropic (Claude)</option>
                <option value="google">Google (AI Studio)</option>
              </select>
            </div>

            {/* Instruction Steps */}
            <div className="bg-black/50 p-4 rounded-lg border border-gray-800 space-y-4">
              <div className="flex items-start">
                <span className="bg-gray-800 rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 flex-shrink-0">2</span>
                <div>
                  <p className="text-sm text-gray-300 mb-1">Open Service in New Tab & Log In</p>
                  <a 
                    href={getServiceUrl()} 
                    target="_blank" 
                    rel="noreferrer"
                    className="text-emerald-500 hover:text-emerald-400 text-xs underline"
                  >
                    Open {getServiceUrl()} ↗
                  </a>
                </div>
              </div>

              <div className="flex items-start">
                <span className="bg-gray-800 rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 flex-shrink-0">3</span>
                <div className="w-full">
                  <p className="text-sm text-gray-300 mb-2 font-bold">Choose Extraction Method:</p>
                  
                  {/* Option A: Bookmarklet */}
                  <div className="mb-4 bg-emerald-900/20 border border-emerald-500/30 p-3 rounded-lg">
                    <p className="text-xs text-emerald-400 font-bold mb-2">Option A: Magic Bookmark (Recommended)</p>
                    <p className="text-xs text-gray-400 mb-2">1. Drag this button to your bookmarks bar:<br/>2. Go to the service tab.<br/>3. Click the bookmark to copy token.</p>
                    <a 
                      href={`javascript:(function(){
                        const c=document.cookie;
                        const k=c.match(/(__Secure-next-auth\.session-token|sessionKey|__Secure-1PSID)=([^;]+)/);
                        if(k){
                          prompt("📋 Token Found! Copy below:", k[2]);
                        }else{
                          alert("❌ Token not found in cookies. Are you logged in?");
                        }
                      })()`}
                      className="inline-block bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3 py-1.5 rounded cursor-grab active:cursor-grabbing border-2 border-dashed border-emerald-400/50"
                      onClick={(e) => e.preventDefault()}
                      title="Drag me to bookmarks bar"
                    >
                      📑 Extract Token
                    </a>
                  </div>

                  {/* Option B: Script */}
                  <div className="border-t border-gray-800 pt-3 opacity-80 hover:opacity-100 transition-opacity">
                    <p className="text-xs text-gray-400 font-bold mb-2">Option B: Console Script</p>
                    <p className="text-[10px] text-gray-500 mb-1">Paste in F12 Console. (If blocked, type "allow pasting")</p>
                    <div className="relative group">
                      <pre className="bg-black border border-gray-800 p-2 rounded text-[10px] text-gray-500 overflow-x-hidden h-12">
                        {extractionScript || '// Loading script...'}
                      </pre>
                      <button 
                        onClick={handleCopyScript}
                        className="absolute top-2 right-2 bg-gray-700 hover:bg-gray-600 text-white px-2 py-1 rounded text-xs flex items-center"
                      >
                        {copied ? <Check className="w-3 h-3 mr-1" /> : <Copy className="w-3 h-3 mr-1" />}
                        {copied ? 'Copied' : 'Copy'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Token Input */}
            <div>
              <label className="block text-xs uppercase text-gray-500 mb-2">4. Paste Captured Token</label>
              <textarea
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Paste the token output here..."
                className="w-full bg-black border border-gray-700 rounded p-3 text-white font-mono text-xs h-24 focus:border-emerald-500 focus:outline-none"
              />
            </div>

            <div className="flex justify-end pt-4">
              <button
                onClick={handleSubmit}
                disabled={loading || !token}
                className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-2 rounded font-bold flex items-center"
              >
                {loading ? 'Securing...' : 'Verify & Save Session'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
