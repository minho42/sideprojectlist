const SortOptionList = ({ data, setData }) => {
  const shuffle = () => {
    const sorted = [...data].sort(() => {
      return Math.random() - 0.5;
    });
    setData(sorted);
  };

  const sortAlphabetically = () => {
    const sorted = [...data].sort((a, b) => {
      return a.fullname > b.fullname ? 1 : a.fullname < b.fullname ? -1 : 0;
    });
    setData(sorted);
  };

  const sortTwitterFollowersCount = () => {
    const sorted = [...data].sort((a, b) => {
      return a.twitter_followers_count < b.twitter_followers_count
        ? 1
        : a.twitter_followers_count > b.twitter_followers_count
        ? -1
        : 0;
    });
    setData(sorted);
  };

  return (
    <div className="flex justify-end">
      <div
        onClick={shuffle}
        className="flex items-center cursor-pointer 
  px-1 py-1 rounded-lg hover:bg-gray-200 sm:ml-2"
      >
        <div className="text-sm hidden sm:flex">Shuffle</div>
        <button className="flex flex-col items-center">
          <svg
            className="w-8 h-8"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            ></path>
          </svg>
          <div className="text-xs flex sm:hidden">Shuffle</div>
        </button>
      </div>

      <div
        onClick={sortAlphabetically}
        className="flex items-center cursor-pointer 
  px-1 py-1 rounded-lg hover:bg-gray-200 sm:ml-2"
      >
        <div className="text-sm hidden sm:flex">A-Z</div>
        <button className="flex flex-col items-center">
          <svg
            className="w-8 h-8"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
            ></path>
          </svg>
          <div className="text-xs flex sm:hidden">A-Z</div>
        </button>
      </div>

      <div
        onClick={sortTwitterFollowersCount}
        className="flex items-center cursor-pointer 
  px-1 py-1 rounded-lg hover:bg-gray-200 sm:ml-2"
      >
        <div className="text-sm hidden sm:flex">Followers</div>
        <button className="flex flex-col items-center">
          <svg
            className="w-8 h-8"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"
            ></path>
          </svg>
          <div className="text-xs flex sm:hidden">Followers</div>
        </button>
      </div>
    </div>
  );
};

export default SortOptionList;
