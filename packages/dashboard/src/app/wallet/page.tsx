"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import BrowserAuthModal from '@/components/wallet/BrowserAuthModal';
import { ArrowLeft, Trash2, Plus, Key, CheckCircle, AlertCircle, Globe } from 'lucide-react';

export default function WalletPage() {
  const [keys, setKeys] = useState<APIKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newKey, setNewKey] = useState({ name: '', key: '', service: 'openai' });
  const [showAddForm, setShowAddForm] = useState(false);
  const [showBrowserAuth, setShowBrowserAuth] = useState(false);

  const fetchKeys = async () => {
    try {
      const res = await fetch('/api/proxy/api/wallet/keys'); // Needs Proxy Check (Updated to 127.0.0.1:8011)
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Fetch Failed: ${res.status} ${res.statusText} - ${text.substring(0, 50)}`);
      }
      const data = await res.json();
      setKeys(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddKey = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/proxy/api/wallet/keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newKey),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to add key');
      }
      setShowAddForm(false);
      setNewKey({ name: '', key: '', service: 'openai' });
      fetchKeys();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Error adding key');
    }
  };

  const handleDeleteKey = async (name: string) => {
    if (!confirm(`Permanently delete key "${name}"?`)) return;
    try {
      const res = await fetch(`/api/proxy/api/wallet/keys/${name}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete key');
      fetchKeys();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Error deleting key');
    }
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  return (
    <div className="min-h-screen bg-black text-white p-8 font-mono">
      <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white mb-8 transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Dashboard
      </Link>

      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400 mb-2">
              Wallet Manager
            </h1>
            <p className="text-gray-500">Secure API Key Storage (Vault)</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setShowBrowserAuth(true)}
              className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center transition-all border border-gray-700"
            >
              <Globe className="w-4 h-4 mr-2" /> Connect via Browser
            </button>
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-md flex items-center transition-all"
            >
              <Plus className="w-4 h-4 mr-2" /> Add Key
            </button>
          </div>
        </div>

        {/* Add Key Form */}
        {showAddForm && (
          <div className="bg-gray-900 border border-emerald-500/30 rounded-lg p-6 mb-8 animate-in fade-in slide-in-from-top-4">
            <h3 className="text-xl font-bold text-emerald-400 mb-4 flex items-center">
              <Key className="w-5 h-5 mr-2" /> New API Key
            </h3>
            <form onSubmit={handleAddKey} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs uppercase text-gray-500 mb-1">Key Name (ID)</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. openai_gpt4"
                    className="w-full bg-black border border-gray-700 rounded p-2 text-white focus:border-emerald-500 focus:outline-none"
                    value={newKey.name}
                    onChange={(e) => setNewKey({ ...newKey, name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase text-gray-500 mb-1">Service Provider</label>
                  <select
                    className="w-full bg-black border border-gray-700 rounded p-2 text-white focus:border-emerald-500 focus:outline-none"
                    value={newKey.service}
                    onChange={(e) => setNewKey({ ...newKey, service: e.target.value })}
                  >
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic</option>
                    <option value="google">Google Gemini</option>
                    <option value="mistral">Mistral</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs uppercase text-gray-500 mb-1">API Key Value</label>
                <input
                  type="password"
                  required
                  placeholder="sk-..."
                  className="w-full bg-black border border-gray-700 rounded p-2 text-white focus:border-emerald-500 focus:outline-none font-mono"
                  value={newKey.key}
                  onChange={(e) => setNewKey({ ...newKey, key: e.target.value })}
                />
              </div>
              <div className="flex justify-end pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="mr-4 text-gray-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2 rounded font-bold"
                >
                  Save Securely
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Key List */}
        {loading ? (
          <div className="text-center py-12 text-gray-500 animate-pulse">Accessing Secure Vault...</div>
        ) : error ? (
          <div className="bg-red-900/20 border border-red-500/50 text-red-400 p-4 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
        ) : keys.length === 0 ? (
          <div className="text-center py-12 text-gray-600 border border-dashed border-gray-800 rounded-lg">
            No keys found in wallet. Add one to get started.
          </div>
        ) : (
          <div className="grid gap-4">
            {keys.map((key) => (
              <div key={key.name} className="bg-gray-900/50 border border-gray-800 hover:border-emerald-500/50 transition-colors p-4 rounded-lg flex justify-between items-center group">
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-4 ${key.access_count > 0 ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]' : 'bg-gray-600'}`}></div>
                  <div>
                    <h3 className="font-bold text-white group-hover:text-emerald-400 transition-colors">{key.name}</h3>
                    <p className="text-xs text-gray-500 uppercase tracking-wider">{key.service} • {key.key_type}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-6">
                  <div className="text-right">
                    <div className="text-xs text-gray-500">Usage</div>
                    <div className="text-sm font-mono text-gray-300">{key.access_count} calls</div>
                  </div>
                  <button
                    onClick={() => handleDeleteKey(key.name)}
                    className="text-gray-600 hover:text-red-500 transition-colors p-2"
                    title="Delete Key"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <BrowserAuthModal 
        isOpen={showBrowserAuth} 
        onClose={() => setShowBrowserAuth(false)}
        onSuccess={fetchKeys}
      />
    </div>
  );
}
