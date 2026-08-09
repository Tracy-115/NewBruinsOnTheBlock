import LorenzoPic from '../assets/NBOTB_Lorenzo.PNG';
import ChristianPic from '../assets/NBOTB_Christian.PNG';
import SuhanaPic from '../assets/NBOTB_Suhana.PNG';
import TracyPic from '../assets/NBOTB_Tracy.PNG';
import vaporwave_bg from '../assets/vaporwave_bg.jpg';
import TeamPic from '../assets/NewBruinsOnTheBlock_photo.PNG';
import { useState } from 'react';

export default function About() {
  const [showIntroductions, setShowIntroductions] = useState(false);

  return (
    <div>
      <h1>About the Creators</h1>
      <p>Click on the photo to learn more about the team!</p>
            {!showIntroductions ? (
        <div className="team-photo">
          <img
            src={TeamPic}
            alt="Picture of New Bruins On The Block"
            onClick={() => setShowIntroductions(true)}
          />
        </div>
      ) : (
        <div className="team">
          <div className="team-member-card-background">
            <img
              className="team-member-image"
              src={LorenzoPic}
              alt="Lorenzo"
            />
            <h3 className="team-member-name">Lorenzo Giron</h3>
            <p className="team-member-bio">
              Hi! My name is Lorenzo, and I am a mechanical engineering
              transfer from Ventura College. My hometown is Oxnard which is
              known for its strawberries, and is also the hometown of Anderson
              .Paak! I enjoy going out for runs, driving down the PCH for fun,
              and watching Korean shows/dramas.
            </p>
          </div>

          <div className="team-member-card-background">
            <img
              className="team-member-image"
              src={ChristianPic}
              alt="Christian"
            />
            <h3 className="team-member-name">Christian Loriega</h3>
            <p className="team-member-bio">
              Hello! My name is Christian, and I'm transferring from Saddleback
              College in Mission Viejo. I'm studying mechanical engineering, and
              I'm interested in aerospace and robotics. During my free time, I
              enjoy working out, building projects, listening to music, and
              eating all-you-can-eat Korean barbecue.
            </p>
          </div>

          <div className="team-member-card-background">
            <img
              className="team-member-image"
              src={SuhanaPic}
              alt="Suhana"
            />
            <h3 className="team-member-name">Suhana Suman</h3>
            <p className="team-member-bio">
              Hi, my name is Suhana and I am a Material Science Engineering
              major transferring from San Diego Miramar College. Some of my
              favorite hobbies are art, especially acrylic painting,
              photography, and designing.
            </p>
          </div>

          <div className="team-member-card-background">
            <img
              className="team-member-image"
              src={TracyPic}
              alt="Tracy"
            />
            <h3 className="team-member-name">
              Kyawt Thinzar (Tracy) Min
            </h3>
            <p className="team-member-bio">
              My name is Kyawt Thinzar (Tracy) Min. I am going to transfer to
              UCLA in Fall 2026 from Diablo Valley College. I am majoring in
              Electrical Engineering and my end goal is to work to implement
              renewable energy in creating digital devices. During my free time,
              I like to cook and visit different neighboring cities.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}