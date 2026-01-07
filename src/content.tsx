import { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { TextScramble } from './components/ui/text-scramble';
import { X, Send } from 'lucide-react';
import './index.css';

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'ai', text: string }[]>([]);
    const [input, setInput] = useState('');
    const [isThinking, setIsThinking] = useState(false);
    const chatAreaRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatAreaRef.current) {
            chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
        }
    }, [messages, isThinking]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const question = input.trim();
        setMessages(prev => [...prev, { role: 'user', text: question }]);
        setInput('');
        setIsThinking(true);

        // Safety check for extension context
        if (typeof chrome === 'undefined' || !chrome.runtime || !chrome.runtime.sendMessage) {
            setIsThinking(false);
            setMessages(prev => [...prev, { role: 'ai', text: "❌ Connection Error: Extension context lost. Please REFRESH this page to re-establish the connection." }]);
            return;
        }

        try {
            chrome.runtime.sendMessage(
                { type: "ASK_QUESTION", question },
                (response: any) => {
                    setIsThinking(false);
                    if (chrome.runtime.lastError) {
                        setMessages(prev => [...prev, { role: 'ai', text: "❌ Extension Error: " + chrome.runtime.lastError?.message + ". Try refreshing the page." }]);
                        return;
                    }

                    if (response && response.success) {
                        setMessages(prev => [...prev, { role: 'ai', text: response.answer }]);
                    } else {
                        setMessages(prev => [...prev, { role: 'ai', text: "❌ Could not connect to backend." }]);
                    }
                }
            );
        } catch (err: any) {
            setIsThinking(false);
            setMessages(prev => [...prev, { role: 'ai', text: "❌ Connection Error: " + err.message }]);
        }
    };

    return (
        <div id="zigmaneural-assistant-container">
            {!isOpen && (
                <div
                    id="ai-chat-toggle"
                    onClick={() => setIsOpen(true)}
                    className="fixed bottom-5 right-5 bg-indigo-600 text-white px-4 py-2 rounded-full cursor-pointer z-[999999] shadow-lg hover:bg-indigo-700 transition-colors font-sans text-sm"
                >
                    Zigma Chat
                </div>
            )}

            {isOpen && (
                <div
                    id="ai-knowledge-sidebar"
                    className="fixed top-0 right-0 w-80 h-screen bg-slate-900 border-l border-slate-700 text-slate-200 z-[999998] flex flex-col shadow-2xl font-sans"
                >
                    <div className="p-4 border-b border-slate-700 flex justify-between items-start">
                        <div className="flex flex-col">
                            <TextScramble
                                text="ZigmaNeural Assistant"
                                className="text-white"
                            />
                            <div className="text-xs text-slate-400 mt-1">Ask company documents</div>
                        </div>
                        <X
                            className="w-5 h-5 cursor-pointer text-slate-400 hover:text-white"
                            onClick={() => setIsOpen(false)}
                        />
                    </div>

                    <div ref={chatAreaRef} className="flex-1 p-4 overflow-y-auto space-y-4 text-sm">
                        {messages.length === 0 && (
                            <div className="text-slate-400 italic text-center mt-10">👋 Ask a question to get answers from company knowledge.</div>
                        )}
                        {messages.map((m, i) => (
                            <div
                                key={i}
                                className={`p-3 rounded-lg ${m.role === 'user' ? 'bg-indigo-600 text-white ml-6' : 'bg-slate-800 text-slate-200 mr-6 border border-slate-700'}`}
                            >
                                <span className="font-bold mr-1">{m.role === 'user' ? 'You:' : 'AI:'}</span>
                                {m.text}
                            </div>
                        ))}
                        {isThinking && (
                            <div className="p-3 rounded-lg bg-slate-800 text-slate-200 mr-6 border border-slate-700 animate-pulse">
                                <span className="font-bold mr-1">AI:</span> Thinking...
                            </div>
                        )}
                    </div>

                    <div className="p-4 border-t border-slate-700 space-y-3">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
                            placeholder="Type your question..."
                            className="w-full h-20 bg-slate-800 border border-slate-700 rounded-md p-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 resize-none"
                        />
                        <button
                            onClick={handleSend}
                            disabled={isThinking}
                            className={`w-full py-2 rounded-md transition-colors flex items-center justify-center gap-2 text-sm font-medium ${isThinking ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                        >
                            <Send className="w-4 h-4" /> Ask
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

const rootDiv = document.createElement('div');
rootDiv.id = 'zigmaneural-root';
document.body.appendChild(rootDiv);

const root = createRoot(rootDiv);
root.render(<Sidebar />);
