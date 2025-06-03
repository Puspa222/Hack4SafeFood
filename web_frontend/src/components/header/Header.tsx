import React from "react";
import { Logo } from "../Logo";

const Header = () => {
  return (
    <div className="flex justify-between">
      <div className=" p-6 bg-gray-800">
        <Logo />
      </div>
      <div className="bg-gray-600">This is Header</div>
    </div>
  );
};

export default Header;
