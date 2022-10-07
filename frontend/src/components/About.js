const About = () => {
  return (
    <div className="flex flex-col items-center justify-center mx-6 pt-4">
      <div className="font-semibold mb-6">A list of awesome personal side projects.</div>
      <div className="mb-4">
        It's like
        <a
          href="https://uses.tech"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-purple-700 hover:text-purple-700 hover:underline px-1"
        >
          uses.tech
        </a>
        but for
        <span className="font-semibold bg-purple-100 py-1 ml-1">/projects.</span>
      </div>

      <div className="mb-2">
        Made by
        <a
          href="https://twitter.com/minhokim42"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-purple-700 hover:text-purple-700 hover:underline ml-1"
        >
          Minho
        </a>
      </div>
    </div>
  );
};

export default About;
