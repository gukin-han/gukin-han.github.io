import React from "react";

const index = () => {
  return (
    <header className="flex justify-between bg-gray-900">
      <h1 className="text-white">Gukin Han</h1>
      <nav>
        <ul className="flex gap-10 text-white">
          <li>About</li>
          <li>
            <a href={`/resume`}>Resume</a>
          </li>
          <li>Portfolio</li>
        </ul>
      </nav>
    </header>
  );
};

export default index;
