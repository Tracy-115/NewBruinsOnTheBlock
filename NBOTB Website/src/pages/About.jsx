import LorenzoPic from '../assets/NBOTB_Lorenzo.PNG';
import ChristianPic from '../assets/NBOTB_Christian.PNG';
import SuhanaPic from '../assets/NBOTB_Suhana.PNG';
import TracyPic from '../assets/NBOTB_Tracy.PNG';

export default function About() {
  return (
    <div>
      <h1>About the Creators</h1>
      <p>Meet the team behind New Bruins On The Block.</p>
      <h1></h1>
      <div className="team">
        <div className="team-member">
          <img className="team-member-image" src={LorenzoPic} alt="Lorenzo" />
          <h3>Lorenzo Giron</h3>
          <p>Hi! My name is Lorenzo, and I am a mechanical engineering transfer from Ventura College. My hometown is Oxnard which is known for its strawberries, and is also the hometown of Anderson .Paak! I enjoy going out for runs, driving down the PCH for fun, and watching Korean shows/dramas.</p>
        </div>
        <div className="team-member">
          <img className="team-member-image" src={ChristianPic} alt="Christian" />
          <h3>Christian Loriega</h3>
          <p>Hello! My name is Christian, and I’m transferring from Saddleback College in Mission Viejo. I’m studying mechanical engineering, and I’m interested in aerospace and robotics. During my free time, I enjoy working out, building projects, listening to music, and eating all-you-can-eat Korean barbecue.</p>
        </div>
        <div className="team-member">
          <img className="team-member-image" src={SuhanaPic} alt="Suhana" />
          <h3>Suhana Suman</h3>
          <p>Hi, my name is Suhana and I am a material science engineering major transferring from San Diego Miramar College. I have recently switched my major from biomedical engineering so my future aspiration is to perhaps implement materials engineering in a medical field. Some of my favorite hobbies are art, especially acrylic painting, photography, and designing.</p>
        </div>
        <div className="team-member">
          <img className="team-member-image" src={TracyPic} alt="Tracy" />
          <h3>Kyawt Thinzar (Tracy) Min</h3>
          <h1> </h1>
          <p>My name is Kyawt Thinzar (Tracy) Min. I am going to transfer to UCLA in Fall 2026 from Diablo Valley College. I am majoring in Electrical Engineering and my end goal is to work to implement renewable energy in creating digital devices. During my free time, I like to cook and visit different neighboring cities.
          </p>
        </div>
      </div>
    </div>
  );
}
