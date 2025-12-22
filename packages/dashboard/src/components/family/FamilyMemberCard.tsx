import React from 'react';
import { User, Heart } from 'lucide-react';

interface FamilyMemberProps {
  name: string;
  role: string;
  avatar_url?: string;
  status: string;
  mood?: string;
}

const FamilyMemberCard: React.FC<FamilyMemberProps> = ({ name, role, avatar_url, status, mood }) => {
  return (
    <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 flex items-center space-x-4 shadow-lg hover:bg-white/15 transition-all">
      <div className="relative">
        <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-purple-400/50 bg-gray-800 flex items-center justify-center">
            {avatar_url ? (
                <img src={avatar_url} alt={name} className="w-full h-full object-cover" />
            ) : (
                <User className="w-8 h-8 text-white/50" />
            )}
        </div>
        <div className={`absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-gray-900 ${
            status === 'active' ? 'bg-green-500' : 'bg-gray-500'
        }`}></div>
      </div>
      
      <div className="flex-1">
        <h3 className="text-lg font-bold text-white tracking-wide">{name}</h3>
        <p className="text-xs text-purple-300 uppercase font-semibold">{role}</p>
        
        <div className="flex items-center mt-2 space-x-2">
            {mood && (
                <span className="px-2 py-0.5 rounded-full bg-pink-500/20 text-pink-300 text-xs border border-pink-500/30 flex items-center gap-1">
                    <Heart className="w-3 h-3" /> {mood}
                </span>
            )}
             <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-xs border border-blue-500/30">
                {status}
            </span>
        </div>
      </div>
    </div>
  );
};

export default FamilyMemberCard;
