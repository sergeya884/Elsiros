package controller.action.ui;

import common.Log;
import controller.action.ActionType;
import controller.action.GCAction;
import data.states.AdvancedData;

public class RetakeGameInterruption  extends GCAction {
    /**
     * Which side has the advantage with this game interruption
     */
    private int side;

    public RetakeGameInterruption(int side) {
        super(ActionType.UI);
        this.side = side;
    }


    @Override
    public void perform(AdvancedData data)
    {
        data.secGameStateInfo.setFreeKickData(data.team[side].teamNumber, (byte) 0);
        data.gameClock.clearSecondaryClock();

        Log.setNextMessage("Retaking: " + data.secGameState.toString() + " " + data.team[side].teamColor.toString());
    }

    @Override
    public boolean isLegal(AdvancedData data) {
        byte[] bytes = data.secGameStateInfo.toByteArray();
        byte team = bytes[0];
        boolean isGoodTeam = team == data.team[side].teamNumber;
        return data.secGameState.isGameInterruption() && isGoodTeam;
    }
}
