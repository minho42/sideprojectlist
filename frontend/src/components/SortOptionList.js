import { RefreshIcon } from "@heroicons/react/outline";
import { SortAscendingIcon } from "@heroicons/react/outline";
import { SortDescendingIcon } from "@heroicons/react/outline";

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

  const optionItems = [
    {
      name: "Shuffle",
      icon: <RefreshIcon className="w-8 h-8" />,

      handleClick: shuffle,
    },
    {
      name: "A-Z",
      icon: <SortAscendingIcon className="w-8 h-8" />,
      handleClick: sortAlphabetically,
    },
    {
      name: "Followers",
      // svgPath: "M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4",
      icon: <SortDescendingIcon className="w-8 h-8" />,

      handleClick: sortTwitterFollowersCount,
    },
  ];

  return (
    <div className="flex justify-end">
      {optionItems.map((item) => {
        return (
          <div
            key={item.name}
            onClick={item.handleClick}
            className="flex items-center cursor-pointer 
  px-1 py-1 rounded-lg hover:bg-gray-200 sm:ml-2"
          >
            <div className="text-sm hidden sm:flex">{item.name}</div>
            <button className="flex flex-col items-center">
              {item.icon}
              <div className="text-xs flex sm:hidden">{item.name}</div>
            </button>
          </div>
        );
      })}
    </div>
  );
};

export default SortOptionList;
