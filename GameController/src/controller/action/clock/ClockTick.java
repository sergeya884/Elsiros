package controller.action.clock;

import controller.action.ActionBoard;
import controller.action.ActionType;
import controller.action.GCAction;
import data.states.AdvancedData;
import data.communication.GameControlData;
import data.Rules;
import data.values.GameStates;
import data.values.GameTypes;
import data.values.SecondaryGameStates;


/**
 * @author Michel Bartsch
 * 
 * This action means that some time has been passed.
 */
public class ClockTick extends GCAction
{
    /**
     * Creates a new ClockTick action.
     * Look at the ActionBoard before using this.
     */
    public ClockTick()
    {
        super(ActionType.CLOCK);
    }

    /**
     * Performs this action to manipulate the data (model).
     * 
     * @param data      The current data to work on.
     */
    @Override
    public void perform(AdvancedData data)
    {
        if (data.gameState == GameStates.READY
               && data.getSecondsSince(data.whenCurrentGameStateBegan) >= Rules.league.readyTime) {
            ActionBoard.set.perform(data);
        } else if (data.gameState == GameStates.FINISHED) {
            Integer remainingPauseTime = data.getRemainingPauseTime();
            if (remainingPauseTime != null) {
                if (data.firstHalf == GameControlData.C_TRUE && remainingPauseTime <= Rules.league.pauseTime / 2 && data.secGameState == SecondaryGameStates.NORMAL) {
                    ActionBoard.secondHalf.perform(data);
                } else if (data.firstHalf == GameControlData.C_TRUE && remainingPauseTime <= Rules.league.pauseOverTime / 2 && data.secGameState == SecondaryGameStates.OVERTIME) {
                    ActionBoard.secondHalfOvertime.perform(data);
                } else if (data.firstHalf != GameControlData.C_TRUE && remainingPauseTime <= Rules.league.pausePenaltyShootOutTime / 2) {
                    ActionBoard.penaltyShoot.perform(data);
                }
            }
        }
        data.updateCoachMessages();
        data.updatePenalties();
    }
    
    /**
     * Checks if this action is legal with the given data (model).
     * Illegal actions are not performed by the EventHandler.
     * 
     * @param data      The current data to check with.
     */
    @Override
    public boolean isLegal(AdvancedData data)
    {
        return true;
    }
    
    public boolean isClockRunning(AdvancedData data)
    {
        boolean halfNotStarted = data.timeBeforeCurrentGameState == 0 && data.gameState != GameStates.PLAYING;
        return !((data.gameState == GameStates.INITIAL)
         || (data.gameState == GameStates.FINISHED)
         || (
                ((data.gameState == GameStates.READY)
               || (data.gameState == GameStates.SET))
                && (((data.gameType == GameTypes.PLAYOFF) && Rules.league.playOffTimeStop) || halfNotStarted)
                )
         || data.manPause)
         || data.manPlay;
    }
}