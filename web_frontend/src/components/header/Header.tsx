import React from "react";
import { Logo } from "../Logo";

const Header = () => {
  return (
    <header className="bg-[#A8C66C] shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Logo />
        <div className="text-gray-800 text-lg font-medium">
          Empowering Nepali Farmers 🌾
        </div>
      </div>
    </header>
  );
};

export default Header;
