package data.hl;

/**
 * This class sets attributes given by the humanoid-league rules.
 *
 * @author Michel-Zen
 */
public class HLSimulationJunior extends HLSim
{
    public HLSimulationJunior()
    {
        /** The league´s name this rules are for. */
        leagueName = "HL Simulation Junior";
        /** The league´s directory name with it´s teams and icons. */
        leagueDirectory = "hl_sim_junior";
        /** How many robots are in a team. */
        teamSize = 2;
        /** How many robots of each team may play at one time. */
        robotsPlaying = 2;
        /** Time in seconds one half is long. */
        halfTime = 5*60;        
        
        /** Time in seconds before a global game stuck can be called. */
        minDurationBeforeStuck = 60;
        /** Time in seconds one overtime half is long. */
        /** SHOULDN'T IT BE CHANGED TO MATCH REGULAR HALF DURATION? */
        overtimeTime = 3*60;

        /** Time in seconds the ready state is long. */
        /** readyTime = 45; */
        /** How long the referee timeout is **/
        /** refereeTimeout = 10*60; */
    }
}
