'use client';

import React from 'react';
import { Lock, Users, Server } from "lucide-react";
import { ROYAL_PERSONAS, ROYAL_LOCKS, SERVICE_PORTS } from '../../config/royal_constants';
import { ROYAL_RULES } from '../../data/royal_rules';

export const RoyalLibrary: React.FC = () => {
  return (
    <section className="py-8 text-slate-700">
      <div className="flex items-center gap-4 mb-8">
        <h2 className="text-xl font-bold text-slate-600">ROYAL LIBRARY & SSOT</h2>
        <div className="h-[1px] flex-1 bg-slate-300"/>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        
        {/* 1. SSOT - Personas */}
        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm">
           <div className="flex items-center justify-between mb-4">
              <h3 className="flex items-center gap-2 font-bold text-slate-600">
                <Users className="w-5 h-5"/> SSOT - Personas
              </h3>
              <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">TRINITY_OS_PERSONAS.yaml</span>
           </div>
           
           <div className="overflow-x-auto">
             <table className="w-full text-sm text-left">
               <thead className="text-xs text-slate-400 uppercase bg-slate-50/50">
                 <tr>
                   <th className="px-4 py-2">Persona</th>
                   <th className="px-4 py-2">Code Name</th>
                   <th className="px-4 py-2">Role</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-slate-100">
                 {ROYAL_PERSONAS.map((p, i) => (
                   <tr key={i} className="hover:bg-white/50">
                     <td className="px-4 py-2 font-medium">{p.name}</td>
                     <td className="px-4 py-2 font-mono text-slate-500">{p.code}</td>
                     <td className="px-4 py-2 text-slate-500">{p.role}</td>
                   </tr>
                 ))}
               </tbody>
             </table>
           </div>
        </div>

        {/* 2. LOCK - Principles */}
        <div className="space-y-6">
           {ROYAL_LOCKS.map((lock, i) => (
               <LockCard key={i} title={lock.title} items={lock.items} color={lock.color} iconColor={lock.iconColor} />
           ))}
        </div>

      </div>



      {/* 3. Port Map */}
      <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm mb-12">
          <div className="flex items-center justify-between mb-4">
              <h3 className="flex items-center gap-2 font-bold text-slate-600">
                <Server className="w-5 h-5"/> Confirmed Stable Paths & Ports
              </h3>
              <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">Active & Listening</span>
          </div>
          <div className="overflow-x-auto">
             <table className="w-full text-sm text-left">
               <thead className="text-xs text-slate-400 uppercase bg-slate-50/50">
                 <tr>
                   <th className="px-4 py-2">Service Component</th>
                   <th className="px-4 py-2">Port</th>
                   <th className="px-4 py-2">Description</th>
                   <th className="px-4 py-2">Status</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-slate-100">
                 {SERVICE_PORTS.map((service, i) => (
                   <tr key={i} className="hover:bg-white/50">
                     <td className="px-4 py-2 font-medium flex items-center gap-2">
                         <div className={`w-2 h-2 rounded-full ${service.service.includes('Soul') ? 'bg-green-500' : 'bg-slate-400'}`}></div>
                         {service.service}
                     </td>
                     <td className="px-4 py-2 font-mono text-slate-600">{service.port}</td>
                     <td className="px-4 py-2 text-slate-500">{service.desc}</td>
                     <td className="px-4 py-2">
                         <span className={`px-2 py-1 text-xs font-bold rounded ${service.color}`}>
                             {service.status}
                         </span>
                     </td>
                   </tr>
                 ))}
               </tbody>
             </table>
           </div>
      </div>

       {/* 4. Royal Rules (Synced from Port 8000) */}
       <div className="space-y-8">
           <div className="flex items-center gap-4">
            <h2 className="text-xl font-bold text-slate-600">IV. ROYAL CONSTITUTION (41 Rules)</h2>
            <div className="h-[1px] flex-1 bg-slate-300"/>
            <span className="text-xs text-slate-400 font-mono">Synced from docs/AFO_ROYAL_LIBRARY.md</span>
           </div>
           
           {ROYAL_RULES.map((book) => (
               <div key={book.id} className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-white/60 shadow-sm">
                   <h3 className="text-lg font-bold text-slate-700 mb-4 border-b border-slate-100 pb-2">{book.title}</h3>
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                       {book.rules.map((rule) => (
                           <div key={rule.id} className="p-4 bg-white rounded-xl border border-slate-100 hover:border-slate-300 transition-colors">
                               <div className="flex justify-between items-start mb-2">
                                   <span className="font-bold text-slate-700 flex items-center gap-2">
                                       <span className="bg-slate-100 text-slate-500 text-xs px-2 py-0.5 rounded-full">#{rule.id}</span>
                                       {rule.name}
                                   </span>
                               </div>
                               <p className="text-sm text-slate-600 mb-3 italic">"{rule.principle}"</p>
                               <div className="bg-slate-900 rounded p-2 overflow-x-auto">
                                   <code className="text-xs font-mono text-green-400 block whitespace-nowrap">
                                       {rule.code}
                                   </code>
                               </div>
                           </div>
                       ))}
                   </div>
               </div>
           ))}
       </div>

    </section>
  );
};

const LockCard = ({ title, items, color, iconColor }: any) => (
  <div className={`p-4 rounded-xl border ${color}`}>
    <h3 className={`flex items-center gap-2 font-bold mb-3 ${iconColor}`}>
      <Lock className="w-4 h-4" /> {title}
    </h3>
    <ul className="space-y-2">
      {items.map((item: string, i: number) => (
        <li key={i} className="flex items-center gap-2 text-sm text-slate-600">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          {item}
        </li>
      ))}
    </ul>
  </div>
);
