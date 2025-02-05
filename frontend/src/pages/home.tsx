import { InteractiveMap } from '../components/interactiveMap.tsx';
import { StaticMap } from '../components/staticMap.tsx';
import { useMap } from '../contexts/mapContext.tsx';
import '../styles/home.css';

export const Home = () => {
    const { currentMap } = useMap();

    return (
        <>
            {currentMap!.name === 'skyrim' && <InteractiveMap />}
            {currentMap!.name !== 'skyrim' && <StaticMap />}
        </>
    );
};
