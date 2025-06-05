import React, { useState } from "react";
import { MessageCircle, X } from "lucide-react";

interface Message {
  message_id: string;
  message: string;
  chat_id: string;
  role: "HUMAN" | "AI";
}

const initialMessages: Message[] = [
  {
    message_id: "1",
    message: "Hello! How can I help you with your farming today?",
    chat_id: "abc123",
    role: "AI",
  },
  {
    message_id: "2",
    message: "What is the best fertilizer for tomatoes?",
    chat_id: "abc123",
    role: "HUMAN",
  },
  {
    message_id: "3",
    message: "Organic compost and neem cake work great for tomatoes.",
    chat_id: "abc123",
    role: "AI",
  },
];

const Chat = () => {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage: Message = {
      message_id: Date.now().toString(),
      message: input,
      chat_id: "abc123",
      role: "HUMAN",
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    // Simulated AI reply
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          message_id: (Date.now() + 1).toString(),
          message: "Thank you! I’ll get back to you with more info.",
          chat_id: "abc123",
          role: "AI",
        },
      ]);
    }, 1000);
  };

  return (
    <>
      {/* Floating Chat Icon */}
      {!open && (
        <button
          className="fixed bottom-6 right-6 bg-[#A8C66C] text-white p-4 rounded-full shadow-lg hover:bg-[#8EB44D] transition z-50"
          onClick={() => setOpen(true)}
        >
          <MessageCircle size={24} />
        </button>
      )}

      {/* Chat Panel */}
      {open && (
        <div className="fixed top-0 right-0 h-full w-full sm:w-[90%] md:w-[70%] lg:w-[50%] xl:w-1/3 bg-white border-l border-gray-300 shadow-xl z-40 flex flex-col transition-all duration-300">
          {/* Header */}
          <div className="bg-[#F3F781] p-4 font-semibold text-lg flex justify-between items-center shadow-sm">
            <span>AI Chat Assistant 🌱</span>
            <button
              onClick={() => setOpen(false)}
              className="hover:text-red-500 transition"
            >
              <X size={24} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg) => (
              <div
                key={msg.message_id}
                className={`w-fit p-3 rounded-xl ${
                  msg.role === "AI"
                    ? "bg-[#E0F7A9] self-start text-left"
                    : "bg-[#DCF8C6] self-end text-right ml-auto"
                }`}
              >
                <span className="text-[15px]">{msg.message}</span>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200 flex gap-2">
            <input
              type="text"
              className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#A8C66C]"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              onClick={handleSend}
              className="bg-[#A8C66C] text-white px-4 py-2 rounded-full hover:bg-[#8EB44D] transition"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chat;
