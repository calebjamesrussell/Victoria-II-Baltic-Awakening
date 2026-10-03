-- Estonia Flavor Mod: engine tuning.
-- Vanilla CONVERSION_SCALE is 0.01; the vanilla religious-conversion engine is
-- the only way POPs change religion day to day. Atheism in this mod spreads
-- through that same engine once the state religion is atheist and same-culture
-- seed POPs exist in a province, so the scale is doubled to make an explicitly
-- secularizing Estonia feel the effect within a campaign.
defines = {
	pops = {
		CONVERSION_SCALE = 0.02
	}
}
