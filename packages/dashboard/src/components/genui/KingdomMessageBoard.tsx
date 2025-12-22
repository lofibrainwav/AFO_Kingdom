import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { LucideCrown, LucidePlus } from 'lucide-react';

interface Message {
  id: string;
  date: string;
  text: string;
}

export function KingdomMessageBoard() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');

  const addMessage = () => {
    if (newMessage.trim()) {
      const now = new Date();
      setMessages([
        ...messages,
        {
          id: Date.now().toString(),
          date: now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }),
          text: newMessage
        }
      ]);
      setNewMessage('');
    }
  };

  return (
    <div className="relative bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl overflow-hidden">
      <div className="absolute inset-0 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl">
        <div className="p-6 md:p-8">
          <div className="flex items-center mb-6">
            <LucideCrown className="w-8 h-8 text-indigo-300 mr-3" />
            <h2 className="text-2xl md:text-3xl font-bold text-white">Commander's Decrees</h2>
          </div>

          <div className="space-y-4 mb-6">
            {messages.map((msg) => (
              <div 
                key={msg.id}
                className="p-5 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300"
              >
                <div className="text-sm text-indigo-200 italic mb-2">{msg.date}</div>
                <p className="text-lg font-medium text-white leading-relaxed">{msg.text}</p>
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            <Input
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Write your decree..."
              className="flex-1 bg-white/5 border border-white/10 text-white placeholder:text-indigo-300"
            />
            <Button
              onClick={addMessage}
              disabled={!newMessage.trim()}
              className="bg-indigo-500 hover:bg-indigo-600 text-white transition-all duration-300"
            >
              <LucidePlus className="w-4 h-4 mr-2" />
              Add Decree
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}