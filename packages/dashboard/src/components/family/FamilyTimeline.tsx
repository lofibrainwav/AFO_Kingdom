import React from 'react';
import { Clock, Star, Zap } from 'lucide-react';

interface ActivityItem {
  id?: string;
  member_id: string;
  activity_type: string;
  description: string;
  impact_score: number;
  timestamp: string;
}

interface FamilyTimelineProps {
  activities: ActivityItem[];
}

const FamilyTimeline: React.FC<FamilyTimelineProps> = ({ activities }) => {
  return (
    <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 shadow-lg h-full">
      <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
        <Clock className="w-5 h-5 text-blue-400" />
        Family Timeline
      </h3>
      
      <div className="space-y-6 relative border-l border-white/10 ml-2 pl-6">
        {activities.map((act, index) => (
          <div key={index} className="relative">
            <div className="absolute -left-[29px] top-1 w-3 h-3 rounded-full bg-purple-500 border-2 border-gray-900 shadow-[0_0_10px_rgba(168,85,247,0.5)]"></div>
            
            <div className="flex justify-between items-start">
                <div>
                    <h4 className="text-white font-semibold text-sm">{act.activity_type}</h4>
                    <p className="text-gray-400 text-xs mt-0.5">{act.description}</p>
                    <p className="text-gray-500 text-[10px] mt-1">{new Date(act.timestamp).toLocaleString()}</p>
                </div>
                {act.impact_score !== 0 && (
                    <span className={`text-xs font-bold px-2 py-0.5 rounded border ${
                        act.impact_score > 0 
                        ? 'bg-green-500/10 text-green-400 border-green-500/30' 
                        : 'bg-red-500/10 text-red-400 border-red-500/30'
                    }`}>
                        {act.impact_score > 0 ? '+' : ''}{act.impact_score}
                    </span>
                )}
            </div>
          </div>
        ))}

        {activities.length === 0 && (
            <div className="text-center text-gray-500 italic py-4">
                No recent activities recorded.
            </div>
        )}
      </div>
    </div>
  );
};

export default FamilyTimeline;
