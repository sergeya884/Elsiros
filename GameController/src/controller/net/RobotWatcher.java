package controller.net;

import controller.EventHandler;
import controller.SystemClock;
import controller.action.ActionBoard;
import controller.action.ui.MakeGoalieAction;
import data.communication.GameControlReturnData;
import data.Rules;
import data.values.Penalties;
import data.values.PlayerResponses;
import data.values.SecondaryGameStates;
import data.values.Side;

/**
 * @author Marcel Steinbeck, Michel Bartsch
 * 
 * You can ask this class about the robots online-status.
 * 
 * This class is a sigleton!
 */
public class RobotWatcher
{
    /** The instance of the singleton. */
    private static RobotWatcher instance = new RobotWatcher();

    /** A timestamp when the last reply from each robot was received. */
    private long [][] robotsLastAnswer = Rules.league.isCoachAvailable ? new long[2][Rules.league.teamSize+1] : new long[2][Rules.league.teamSize];
    /** Last message reeived from each robot.
     *  Look at GameControlReturnData for information about messages */
    private PlayerResponses[][] robotsLastMessage = Rules.league.isCoachAvailable ? new PlayerResponses[2][Rules.league.teamSize+1] : new PlayerResponses[2][Rules.league.teamSize];
    /** The calculated information about the online-status. */
    private RobotOnlineStatus [][] status = Rules.league.isCoachAvailable ? new RobotOnlineStatus[2][Rules.league.teamSize+1] : new RobotOnlineStatus[2][Rules.league.teamSize];

    /** What the constants name says. */
    private final static int MILLIS_UNTIL_ROBOT_IS_OFFLINE = 4*1000;
    private final static int MILLIS_UNTIL_ROBOT_HAS_HIGH_LATANCY = 2*1000;

    /**
     * Creates a new RobotWatcher.
     */
    private RobotWatcher()
    {
        for (int i  = 0; i < 2; i++) {
            for (int j = 0; j < Rules.league.teamSize; j++) {
                robotsLastMessage[i][j] = PlayerResponses.MAN_PENALISE;
                status[i][j] = RobotOnlineStatus.UNKNOWN;
            }
            if (Rules.league.isCoachAvailable) {
                status[i][Rules.league.teamSize] = RobotOnlineStatus.UNKNOWN;
            }
        }
    }
    
    /**
     * Recieves robot´s answers to update corresponding timestamps and fire
     * actions caused manual on the robot.
     * 
     * @param gameControlReturnData     The robot`s answer.
     */
    public static synchronized void update(GameControlReturnData gameControlReturnData)
    {
        int team, number;
        if (gameControlReturnData.team == EventHandler.getInstance().data.team[0].teamNumber) {
            team = 0;
        } else if (gameControlReturnData.team == EventHandler.getInstance().data.team[1].teamNumber) {
            team = 1;
        } else {
            return;
        }
        number = gameControlReturnData.player;
        if (number <= 0 || number > Rules.league.teamSize) {
            return;
        }
        instance.robotsLastAnswer[team][number-1] = SystemClock.getInstance().getCurrentTimeMillis();
        if (instance.robotsLastMessage[team][number-1] != gameControlReturnData.message) {
            instance.robotsLastMessage[team][number-1] = gameControlReturnData.message;
            if ((gameControlReturnData.message == PlayerResponses.MAN_PENALISE)
                    && (EventHandler.getInstance().data.team[team].player[number-1].penalty == Penalties.NONE)) {
                ActionBoard.manualPen[team][number-1].actionPerformed(null);
            } else if ((gameControlReturnData.message == PlayerResponses.MAN_UNPENALISE)
                    && (EventHandler.getInstance().data.team[team].player[number-1].penalty != Penalties.NONE)) {
                ActionBoard.manualUnpen[team][number-1].actionPerformed(null);
            }} else if (gameControlReturnData.message == PlayerResponses.GOALKEEPER) {
                MakeGoalieAction makeGoalie = new MakeGoalieAction(Side.getFromInt(team), number-1);
                    if(makeGoalie.isLegal(EventHandler.getInstance().data)) {
                        makeGoalie.perform(EventHandler.getInstance().data);
                    }
            }  else if (gameControlReturnData.message == PlayerResponses.GAME_INTERRUPTION_READY) {
                if (EventHandler.getInstance().data.secGameStateInfo.toByteArray()[1] == 1 // we are currently in the preparation phase
                        && EventHandler.getInstance().data.secGameStateInfo.toByteArray()[0] == gameControlReturnData.team) { // the robot is from the team begin allowed to execute the game interruption
                    if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.DIRECT_FREEKICK
                            && ActionBoard.directFreeKick[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.directFreeKick[team].perform(EventHandler.getInstance().data);
                    } else if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.INDIRECT_FREEKICK
                            && ActionBoard.indirectFreeKick[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.indirectFreeKick[team].perform(EventHandler.getInstance().data);
                    } else if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.CORNER_KICK
                            && ActionBoard.cornerKick[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.cornerKick[team].perform(EventHandler.getInstance().data);
                    } else if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.GOAL_KICK
                            && ActionBoard.goalKick[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.goalKick[team].perform(EventHandler.getInstance().data);
                    } else if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.THROW_IN
                            && ActionBoard.throwIn[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.throwIn[team].perform(EventHandler.getInstance().data);
                    } else if (EventHandler.getInstance().data.secGameState == SecondaryGameStates.PENALTYKICK
                            && ActionBoard.penaltyKick[team].isLegal(EventHandler.getInstance().data)) {
                        ActionBoard.penaltyKick[team].perform(EventHandler.getInstance().data);
                    }
                }
        }
    }

    /**
     * Calculates new online-status for each robot.
     * 
     * @return The updated online-status of each robot.
     */
    public static synchronized RobotOnlineStatus[][] updateRobotOnlineStatus()
    {
        long currentTime = SystemClock.getInstance().getCurrentTimeMillis();
        int robotsOffline;
        for (int i=0; i<2; i++) {
            robotsOffline = 0;
            for (int j=0; j < instance.status[i].length; j++) {
                if (currentTime - instance.robotsLastAnswer[i][j] > MILLIS_UNTIL_ROBOT_IS_OFFLINE) {
                    instance.status[i][j] = RobotOnlineStatus.OFFLINE;
                    if (++robotsOffline >= Rules.league.teamSize + (Rules.league.isCoachAvailable ? 1 : 0)) {
                        for (int k=0; k < Rules.league.teamSize; k++) {
                            instance.status[i][k] = RobotOnlineStatus.UNKNOWN;
                        }
                        if (Rules.league.isCoachAvailable) {
                            instance.status[i][Rules.league.teamSize] = RobotOnlineStatus.UNKNOWN;
                        }
                    }
                } else if (currentTime - instance.robotsLastAnswer[i][j] > MILLIS_UNTIL_ROBOT_HAS_HIGH_LATANCY) {
                    instance.status[i][j] = RobotOnlineStatus.HIGH_LATENCY;
                } else {
                    instance.status[i][j] = RobotOnlineStatus.ONLINE;
                }
            }
        }
        return instance.status;
    }
    
    public static synchronized void updateCoach(byte team)
    {
        instance.robotsLastAnswer[team][Rules.league.teamSize] = SystemClock.getInstance().getCurrentTimeMillis();
    }
}